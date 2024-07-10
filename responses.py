import ujson
import typing
from starlette.responses import JSONResponse

class UJSONResponse(JSONResponse):
  
  def render(self, content: typing.Any) -> bytes:
    return ujson.dumps(content).encode('utf-8')