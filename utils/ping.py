from asyncioping import ping

async def ping_server(ip):
    if ip == 'not here':
        return 'Not Here', 'N/A'
    try:
        response_time = await ping(ip)
        return 'Online', f'{response_time * 1000:.2f} ms'
    except TimeoutError:
        return 'Offline', 'N/A'
    except Exception:
        return 'Erreur lors du ping', 'N/A'