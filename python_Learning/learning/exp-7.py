
import httpx
from httpx_socks import SyncProxyTransport

# 替换为你的代理地址（SOCKS/HTTP都可以）
transport = SyncProxyTransport.from_url('socks5://127.0.0.1:7897')
client = httpx.Client(transport=transport)

# 测试访问coze的公开接口（无需API Key）
try:
    resp = client.get('https://www.coze.com')
    print(f'代理访问成功！状态码：{resp.status_code}')
except Exception as e:
    print(f'代理访问失败：{str(e)}')

