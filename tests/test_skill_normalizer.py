from app.services.skill_normalizer import normalize_skill


def test_normalize_docker_containerization():
    assert (
        normalize_skill("docker containerization")
        == "Docker"
    )


def test_normalize_k8s():
    assert (
        normalize_skill("k8s")
        == "Kubernetes"
    )


def test_normalize_unknown_skill():
    assert (
        normalize_skill("Python")
        == "Python"
    )
