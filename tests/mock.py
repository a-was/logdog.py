import io


class MockStream(io.StringIO):
    def getvalue(self) -> str:
        v = super().getvalue()
        self.seek(0)
        self.truncate(0)
        return v.rstrip("\n")
