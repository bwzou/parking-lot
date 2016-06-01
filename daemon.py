"""
coding by Zuo Dexin
"""
from Parking import app
import RedisQueue
RedisQueue.queue_daemon(app)