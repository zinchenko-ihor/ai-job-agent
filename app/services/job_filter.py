class JobFilter:

    # Roles that are directly relevant to DevOps / infrastructure.
    DEVOPS_TITLE_KEYWORDS = [
        "devops",
        "site reliability",
        "sre",
        "platform engineer",
        "platform engineering",
        "cloud engineer",
        "cloud operations engineer",
        "cloud operations",
        "cloud infrastructure",
        "infrastructure engineer",
        "infrastructure engineering",
        "systems engineer",
        "system engineer",
        "system administrator",
        "systems administrator",
        "linux administrator",
        "release engineer",
        "build engineer",
        "deployment engineer",
        "automation engineer",
        "devsecops",
        "cloudops",
    ]

    # Support roles are accepted only when their description
    # contains at least one DevOps-relevant technology.
    SUPPORT_TITLE_KEYWORDS = [
        "technical support engineer",
        "technical support",
        "it support engineer",
        "it support",
        "systems support engineer",
        "system support engineer",
        "infrastructure support engineer",
        "infrastructure support",
        "cloud support engineer",
        "cloud support",
        "application support engineer",
        "production support engineer",
        "production support",
        "support engineer",
    ]

    DEVOPS_STACK_KEYWORDS = [
        # Operating systems
        "linux",
        "unix",

        # Cloud
        "aws",
        "amazon web services",
        "azure",
        "gcp",
        "google cloud",
        "cloud infrastructure",

        # Containers / orchestration
        "docker",
        "kubernetes",
        "k8s",
        "containerization",

        # Infrastructure as Code / automation
        "terraform",
        "ansible",
        "puppet",
        "chef",
        "vagrant",

        # CI/CD
        "ci/cd",
        "cicd",
        "continuous integration",
        "continuous delivery",
        "jenkins",
        "gitlab ci",
        "github actions",
        "azure devops",

        # Monitoring / observability
        "prometheus",
        "grafana",
        "zabbix",
        "elk",
        "elk stack",
        "elastic stack",
        "elasticsearch",
        "logstash",
        "kibana",
        "loki",
        "observability",
        "monitoring",

        # Web / infrastructure
        "nginx",
        "haproxy",

        # Networking
        "networking",
        "tcp/ip",
        "tcp ip",
        "dns",
        "vpn",
        "firewall",
        "load balancer",
        "routing",

        # Automation / scripting
        "bash",
        "shell scripting",
        "shell script",
        "powershell",
        "automation",

        # Infrastructure / operations
        "infrastructure",
        "deployment",
        "production environment",
        "production systems",
        "system administration",
        "systems administration",
        "cloud operations",
        "infrastructure operations",
    ]

    EXCLUDED_TITLE_KEYWORDS = [
        # Hospitality
        "barista",
        "waiter",
        "waitress",
        "chef",
        "cook",
        "bartender",

        # Sales / business
        "sales manager",
        "sales representative",
        "sales specialist",
        "account manager",
        "business development",
        "business development manager",

        # Customer service
        "customer service",
        "customer support",
        "customer success",

        # HR / recruiting
        "recruiter",
        "recruitment",
        "talent acquisition",
        "hr manager",
        "human resources",

        # Marketing / content
        "marketing",
        "designer",
        "copywriter",
        "content writer",

        # Healthcare / education / legal
        "teacher",
        "nurse",
        "doctor",
        "lawyer",
        "accountant",

        # Other software roles that we explicitly don't want
        "frontend developer",
        "front-end developer",
        "backend developer",
        "back-end developer",
        "full stack developer",
        "full-stack developer",
        "mobile developer",
        "ios developer",
        "android developer",
        "data engineer",
        "data scientist",
        "machine learning engineer",
        "ml engineer",
        "qa engineer",
        "qa automation engineer",
        "test automation engineer",
        "software engineer",
        "software developer",
    ]

    def is_relevant(
        self,
        title: str,
        description: str = "",
    ) -> bool:

        title_text = (title or "").lower().strip()
        description_text = (description or "").lower()

        # ---------------------------------------------------------
        # 1. Reject clearly unrelated roles first.
        # ---------------------------------------------------------

        for keyword in self.EXCLUDED_TITLE_KEYWORDS:
            if keyword in title_text:
                return False

        # ---------------------------------------------------------
        # 2. Direct DevOps / infrastructure role.
        # ---------------------------------------------------------

        for keyword in self.DEVOPS_TITLE_KEYWORDS:
            if keyword in title_text:
                return True

        # ---------------------------------------------------------
        # 3. Technical / IT support role.
        #
        # Support roles are accepted ONLY when the description
        # contains DevOps-relevant technologies.
        # ---------------------------------------------------------

        is_support_role = any(
            keyword in title_text
            for keyword in self.SUPPORT_TITLE_KEYWORDS
        )

        if is_support_role:

            for keyword in self.DEVOPS_STACK_KEYWORDS:
                if keyword in description_text:
                    return True

            return False

        # ---------------------------------------------------------
        # 4. Generic title.
        #
        # We do NOT accept arbitrary jobs just because their
        # description mentions Docker / AWS / etc.
        #
        # This prevents things like:
        # "Software Engineer" + AWS
        # "Data Engineer" + Kubernetes
        # from entering the DevOps pipeline.
        # ---------------------------------------------------------

        return False
