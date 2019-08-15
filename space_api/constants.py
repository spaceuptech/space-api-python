MySQL = 'sql-mysql'
Postgres = 'sql-postgres'
Mongo = 'mongo'


# TypeServiceRegister is the request type for service registration
TypeServiceRegister = "service-register"
# TypeServiceUnregister is the request type for service removal
TypeServiceUnregister = "service-unregister"
# TypeServiceRequest is type triggering a service's function
TypeServiceRequest = "service-request"

Insert = "insert"
Write = "write"
Delete = "delete"
Update = "update"
Initial = "initial"

# TypeRealtimeSubscribe is the request type for live query subscription
TypeRealtimeSubscribe = "realtime-subscribe"
# TypeRealtimeUnsubscribe is the request type for live query subscription
TypeRealtimeUnsubscribe = "realtime-unsubscribe"
# TypeRealtimeFeed is the response type for realtime feed
TypeRealtimeFeed = "realtime-feed"

# PayloadSize is the size of the payload(in bytes) in file upload and download
PayloadSize = 256 * 1024  # 256 kB

# TypePubsubSubscribe is type triggering a pubsub subscribe
TypePubsubSubscribe = "pubsub-subscribe"

# TypePubsubSubscribeFeed is type having a pubsub subscribe feed
TypePubsubSubscribeFeed = "pubsub-subscribe-feed"

# TypePubsubUnsubscribe is type triggering a pubsub unsubscribe
TypePubsubUnsubscribe = "pubsub-unsubscribe"

# TypePubsubUnsubscribeAll is type triggering a pubsub unsubscribe all
TypePubsubUnsubscribeAll = "pubsub-unsubscribe-all"
