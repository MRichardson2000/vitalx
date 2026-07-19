from pathlib import Path

DBO = (Path(__file__).parent.parent.parent / "dbo").resolve()
CREATES_DBO = DBO / "creates"
ANALYTICS_DBO = DBO / "analytics"
