from playwright.sync_api import sync_playwright
from datetime import datetime

'''
This is a automation script that goes to any arc cinema locations website,
visits each showing for today, and returns the amount of seats sold.
It then uses an average amount of seats sold per screening to deteremine how busy it will be from the time the script is ran onwards.
'''


def seats_counter():
    # Date import to make sure we're looking at todays screenings
    now = datetime.now()
    today = f"{now.day} {now.strftime('%B')}"

    messages = []

    # Initialise playwright
    with sync_playwright() as p:
        # Headless browser as GUI not needed
        browser = p.chromium.launch(headless=True)
        # Launch a browser page in this browser instance
        page = browser.new_page()

        # INSERT LINK TO DESIRED ARC CINEMAS WHATS ON PAGE
        page.goto("https://LOCATION.arccinema .ie OR .co.uk/whatson")

        # wait for page to load
        page.wait_for_selector("#panels .whatson_panel.block a.perfButton")

        # Find date on page
        page_date = (
            page.locator("#selectedDateDisplay")
            .inner_text()
            .strip()
        )

        # If todays date doesn't match the date shown on the page, close instance
      #  if page_date.upper() != page_date.upper():
       #     browser.close()
       #     return ["Today's listings not available."]

        links = page.locator(
            "#panels .whatson_panel.block a.perfButton"
        ).evaluate_all(
            "els => els.map(e => e.href)"
        )

        number_of_screenings = len(links)

        total_seats_sold = 0
        # Go to links and wait for seats to load(class us, as)
        for link in links:
            page.goto(link)
            page.wait_for_selector(
                'span[class^="us_"], span[class^="as_"]'
            )
            # The class "us" stands for unavailable seat, a seat which has been purchased. the scraper looks for these in each showing
            sold = page.locator('span[class^="us_"]').count()
            total_seats_sold += sold

        browser.close()

    if number_of_screenings == 0:
        return ["No screenings found."]

    average = total_seats_sold // number_of_screenings

    messages.append(f"Screenings left today: {number_of_screenings}")
    # Seats sold is not a good indicator of business as there is a possibility that not all screenings will show up if it later in the day
    messages.append(f"Total seats sold: {total_seats_sold}")
    # Using average number of seats per screen is a better indicator of busyness
    messages.append(f"Average per screen: {average}")

  # appending different statements to a list so that the bot can use them within the average seats sold parameter
    if average <= 4:
        messages.append("Absolutely dead so far")
    elif average <= 10:
        messages.append("Not too busy")
    elif average <= 15:
        messages.append("A healthy stream of customers")
    elif average <= 20:
        messages.append("Busy enough")
    elif average <= 25:
        messages.append("Busy busy bees")
    elif average <= 30:
        messages.append("Super busy")
    elif average <= 35:
        messages.append("Really really super busy")
    elif average <= 40:
        messages.append("No time to think, just go")
    else:
        messages.append("May the cinema gods have mercy on us")

    for i in messages:
        print(i)

    return messages


seats_counter()
