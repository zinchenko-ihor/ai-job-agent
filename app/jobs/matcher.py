from __future__ import annotations

import re
from typing import Any


class JobMatcher:
    """
    Deterministic job matcher.

    Scores:
    - Role match:       30
    - Skills match:     50
    - DevOps bonus:     10
    - Seniority:        10

    Filters:
    - English above B1 rejected
    """


    ROLE_KEYWORDS = {
        "devops",
        "sre",
        "site reliability",
        "platform engineer",
        "cloud engineer",
        "cloud operations",
        "infrastructure engineer",
        "system administrator",
        "sysadmin",
        "operations engineer",
        "technical support",
        "application support",
    }


    SKILLS = {
        "linux",
        "ubuntu",
        "oracle linux",
        "windows server",

        "aws",
        "ec2",
        "iam",
        "s3",
        "cloudwatch",

        "docker",
        "kubernetes",
        "terraform",

        "ansible",
        "jenkins",
        "github actions",
        "gitlab ci",

        "prometheus",
        "grafana",
        "zabbix",
        "kibana",
        "elasticsearch",

        "nginx",
        "apache",

        "bash",
        "powershell",
        "python",

        "git",

        "postgresql",
        "mysql",
        "mssql",

        "dns",
        "dhcp",
        "vpn",
        "networking",
    }


    ENGLISH_LEVELS = {
        "a1": 1,
        "a2": 2,
        "b1": 3,
        "b2": 4,
        "c1": 5,
        "c2": 6,
    }


    MAX_ENGLISH = 3



    def match(
        self,
        profile: dict[str, Any],
        job: dict[str, Any],
    ) -> dict[str, Any]:


        title = (
            str(job.get("title", ""))
            .lower()
        )


        description = (
            str(job.get("description", ""))
            .lower()
        )


        text = (
            title
            +
            " "
            +
            description
        )


        #
        # English filter
        #

        english = self._detect_english(text)


        if (
            english
            and
            english > self.MAX_ENGLISH
        ):

            return self._result(
                False,
                0,
                "English level above B1",
                [],
                [],
            )



        #
        # Candidate skills
        #

        candidate_skills = (
            self._normalize_profile_skills(
                profile
            )
        )


        #
        # Job skills
        #

        job_skills = (
            self._extract_skills(
                text
            )
        )


        matched_skills = sorted(
            candidate_skills
            &
            job_skills
        )


        missing_skills = sorted(
            job_skills
            -
            candidate_skills
        )


        #
        # Role score
        #

        role_score = 0


        for role in profile.get(
            "target_roles",
            []
        ):

            normalized = (
                role.lower()
            )

            if (
                normalized in title
                or
                any(
                    keyword in title
                    for keyword in self.ROLE_KEYWORDS
                )
            ):
                role_score = 30
                break



        #
        # Skill score
        #

        skill_score = 0


        if job_skills:

            ratio = (
                len(matched_skills)
                /
                len(job_skills)
            )

            skill_score = round(
                ratio * 50
            )



        #
        # DevOps bonus
        #

        devops_bonus = min(
            len(
                matched_skills
            ),
            10,
        )



        #
        # Seniority
        #

        seniority_score = (
            self._seniority_score(
                profile,
                title,
            )
        )



        score = min(
            role_score
            +
            skill_score
            +
            devops_bonus
            +
            seniority_score,
            100,
        )



        matched = (
            score >= 25
            and
            len(matched_skills) >= 1
        )



        return self._result(
            matched,
            score,
            self._reason(
                matched_skills,
                role_score,
            ),
            matched_skills,
            missing_skills,
        )



    # ==================================================
    # NORMALIZATION
    # ==================================================


    def _normalize_profile_skills(
        self,
        profile: dict[str, Any],
    ) -> set[str]:


        result = set()


        all_sources = []


        for key in [
            "skills",
            "devops",
            "cloud",
            "monitoring",
            "databases",
            "operating_systems",
            "networking",
        ]:

            values = profile.get(
                key,
                []
            )


            if isinstance(
                values,
                list
            ):
                all_sources.extend(
                    values
                )



        for item in all_sources:

            text = (
                str(item)
                .lower()
            )


            for skill in self.SKILLS:

                if skill in text:

                    result.add(
                        skill
                    )


        return result



    def _extract_skills(
        self,
        text: str,
    ) -> set[str]:

        result = set()


        for skill in self.SKILLS:

            if skill in text:

                result.add(
                    skill
                )


        return result



    # ==================================================
    # HELPERS
    # ==================================================


    def _detect_english(
        self,
        text: str,
    ) -> int | None:


        patterns = {

            "c1": [
                r"\bc1\b",
                "fluent",
                "advanced",
            ],

            "b2": [
                r"\bb2\b",
                "upper intermediate",
            ],

            "b1": [
                r"\bb1\b",
                "intermediate",
            ],

        }


        for level, values in patterns.items():

            for pattern in values:

                if re.search(
                    pattern,
                    text,
                    re.I,
                ):
                    return self.ENGLISH_LEVELS[level]


        return None



    def _seniority_score(
        self,
        profile: dict[str, Any],
        title: str,
    ) -> int:


        candidate = (
            str(
                profile.get(
                    "seniority",
                    ""
                )
            )
            .lower()
        )


        if "senior" in title:

            if candidate == "senior":
                return 10

            return 5



        if (
            "middle" in title
            or
            "mid" in title
        ):

            if candidate in [
                "mid",
                "middle",
                "senior",
            ]:
                return 10



        return 5



    def _reason(
        self,
        skills: list[str],
        role_score: int,
    ) -> str:


        result = []


        if role_score:
            result.append(
                "role match"
            )


        if skills:
            result.append(
                f"{len(skills)} skills matched"
            )


        if not result:
            return "weak match"


        return ", ".join(result)



    def _result(
        self,
        matched: bool,
        score: int,
        reason: str,
        matched_skills: list[str],
        missing_skills: list[str],
    ) -> dict[str, Any]:

        return {
            "matched": matched,
            "score": score,
            "reason": reason,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
        }
