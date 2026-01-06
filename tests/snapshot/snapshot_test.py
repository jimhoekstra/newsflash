from pathlib import Path


class SnapshotTest:

    name: str = ""
    path_to_rendered: Path
    description: str = ""

    @staticmethod
    def render() -> str:
        ...

    @classmethod
    def snapshot_exists(cls) -> bool:
        return cls.path_to_rendered.exists()
    
    @classmethod
    def load_rendered(cls) -> str | None:
        if cls.snapshot_exists():
            return cls.path_to_rendered.read_text()
        else:
            return None
    
    @classmethod
    def save_rendered(cls, content: str) -> None:
        rendered = cls.render()
        assert rendered == content, "Rendered content does not match provided content."

        cls.path_to_rendered.parent.mkdir(parents=True, exist_ok=True)
        cls.path_to_rendered.write_text(rendered)

    @classmethod
    def passes_test(cls, content: str | None = None) -> bool:
        if not cls.snapshot_exists():
            return False
    
        snapshot = cls.load_rendered()
        assert snapshot is not None
        rendered = cls.render()
        if content is not None:
            assert rendered == content, "Rendered content does not match provided content."

        return snapshot == rendered
