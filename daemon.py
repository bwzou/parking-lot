from Parking import app
import RedisQueue
RedisQueue.queue_daemon(app)