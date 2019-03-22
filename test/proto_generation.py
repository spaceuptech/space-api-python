from space_api.proto import server_pb2
import json

project = 'project'
db_type = 'sql'
col = 'collection'

meta = server_pb2.Meta(project=project, dbType=db_type, col=col, token=None)

find = b'asdf'
operation = 'op'
delete_request = server_pb2.DeleteRequest(find=find, operation=operation, meta=meta)

for t in [{'a': 25, 'adf': 'asdf'}, 'as', ['df'], 25]:
    find = json.dumps(t, separators=(',', ':')).encode('utf-8')
    print(find)
    print(t, json.loads(find))
    print(t == json.loads(find))
exit(0)
operation = 'op'
delete_request = server_pb2.DeleteRequest(find=find, operation=operation, meta=meta)
# print(delete_request)

select = {'df': 2}
sort = {'df': 2}
read_options = server_pb2.ReadOptions(select=select, sort=sort, skip=511515, limit=511515, distinct='distinct')
print(read_options)
print(read_options.sort == sort)
print(read_options.select == select)