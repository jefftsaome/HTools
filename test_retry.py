import asyncio
from htools.utils.retry import async_retry, retryable

# Test async_retry: first fail, second succeed
call_count = 0
async def flaky():
    global call_count
    call_count += 1
    if call_count < 2:
        raise ValueError('not yet')
    return 'ok'

result = asyncio.run(async_retry(flaky, max_retries=2, base_delay=0.01))
assert result == 'ok'
assert call_count == 2

# Test retryable decorator
call_count2 = 0
@retryable(max_retries=2, base_delay=0.01)
async def flaky2():
    global call_count2
    call_count2 += 1
    if call_count2 < 2:
        raise ValueError('not yet')
    return 'ok'

result2 = asyncio.run(flaky2())
assert result2 == 'ok'
assert call_count2 == 2

print('retry OK')
