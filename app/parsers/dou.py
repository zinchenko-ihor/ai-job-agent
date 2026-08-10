import re

from datetime import datetime, timezone

from bs4 import BeautifulSoup


class DOUJobParser:

    @staticmethod
    def parse(html: str) -> list[dict]:

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        jobs = []

        for vacancy in soup.select(
            "li.l-vacancy"
        ):

            title_element = vacancy.select_one(
                "a.vt"
            )

            company_element = vacancy.select_one(
                "a[href*='/companies/']"
            )

            location_element = vacancy.select_one(
                ".cities"
            )

            date_element = vacancy.select_one(
                ".date"
            )

            if not title_element:
                continue

            title = title_element.get_text(
                " ",
                strip=True,
            )

            url = title_element.get(
                "href"
            )

            company = None

            if company_element:
                company = company_element.get_text(
                    " ",
                    strip=True,
                )

            location = None

            if location_element:
                location = location_element.get_text(
                    " ",
                    strip=True,
                )

            published_at = (
                DOUJobParser.parse_date(
                    date_element
                )
            )

            description = (
                DOUJobParser.extract_description(
                    vacancy
                )
            )

            external_id = (
                DOUJobParser.extract_external_id(
                    url
                )
            )

            jobs.append(
                {
                    "external_id": external_id,
                    "title": title,
                    "company": company,
                    "location": location,
                    "employment_type": None,
                    "description": description,
                    "url": url,
                    "published_at": published_at,
                    "salary_min": None,
                    "salary_max": None,
                    "currency": None,
                }
            )

        return jobs

    @staticmethod
    def parse_date(
        date_element,
    ) -> datetime | None:

        if not date_element:
            return None

        text = date_element.get_text(
            " ",
            strip=True,
        )

        if not text:
            return None

        # DOU normally uses dates such as:
        #
        # 27 липня
        # 07 липня
        #
        # For MVP we use the current year.

        match = re.search(
            r"(\d{1,2})\s+([а-яіїєґ]+)",
            text.lower(),
        )

        if not match:
            return None

        day = int(
            match.group(1)
        )

        month_name = match.group(2)

        months = {
            "січня": 1,
            "лютого": 2,
            "березня": 3,
            "квітня": 4,
            "травня": 5,
            "червня": 6,
            "липня": 7,
            "серпня": 8,
            "вересня": 9,
            "жовтня": 10,
            "листопада": 11,
            "грудня": 12,
        }

        month = months.get(
            month_name
        )

        if not month:
            return None

        return datetime(
            year=datetime.now(
                timezone.utc
            ).year,
            month=month,
            day=day,
            tzinfo=timezone.utc,
        )

    @staticmethod
    def extract_description(
        vacancy,
    ) -> str | None:

        element = vacancy.select_one(
            ".l-vacancy__body"
        )

        if not element:
            element = vacancy.select_one(
                ".sh-info"
            )

        if not element:
            return None

        return element.get_text(
            "\n",
            strip=True,
        )

    @staticmethod
    def extract_external_id(
        url: str | None,
    ) -> str | None:

        if not url:
            return None

        match = re.search(
            r"/vacancies/(\d+)",
            url,
        )

        if match:
            return match.group(1)

        return url
