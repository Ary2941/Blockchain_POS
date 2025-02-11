import requests,threading,time

from datetime import datetime
import pytz
#se não tiver internet, vai o horário do celular mesmo :p
def get_local_datetime():
    # Obtendo o fuso horário do sistema (no caso, América/São Paulo)
    local_time = datetime.now()
    # Criando um objeto datetime com os valores de ano, mês, dia, hora, minuto, segundo, milissegundos
    naive = datetime(
        local_time.year,
        local_time.month,
        local_time.day,
        local_time.hour,
        local_time.minute,
        local_time.second,
        local_time.microsecond // 1000 * 1000,  # Convertendo microssegundos para milissegundos
    )

    aware = pytz.timezone('America/Sao_Paulo').localize(naive)
    return aware

#https://timeapi.io/api/Time/current/zone?timeZone=America/Sao_Paulo
def fetch_timeapi():
    global timeapi
    timeapi = get_time_from_timeapi("America/Sao_Paulo")
def get_time_from_timeapi(timezone="America/Sao_Paulo"):
    url = f'https://timeapi.io/api/time/current/zone?timeZone={timezone}'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Lança um erro se o status for ruim
        data = response.json()        
        # Obtendo a data e hora em formato ISO 8601
        datetime_str = data.get("dateTime", "Erro ao obter horário")
        
        if datetime_str != "Erro ao obter horário":
            # Convertendo para datetime
            dt = datetime.fromisoformat(datetime_str)

            # Criando o dicionário no formato desejado
            time_data = {
                'year': dt.year,
                'month': dt.month,
                'day': dt.day,
                'hour': dt.hour,
                'minute': dt.minute,
                'seconds': dt.second,
                'milliSeconds': dt.microsecond // 1000,  # Convertendo microssegundos para milissegundos
                'timeZone': timezone
            }
            
            return time_data
        
        return None
    except requests.exceptions.RequestException as e:
        return None

#https://httpbin.org/get
def get_time_from_httpbin(timezone='America/Sao_Paulo'):
    url = "https://httpbin.org/get"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        server_time = response.headers.get("Date", "Erro ao obter horário")
        
        if server_time != "Erro ao obter horário":
            # Convertendo o horário de UTC para o fuso horário
            utc_time = datetime.strptime(server_time, '%a, %d %b %Y %H:%M:%S %Z')
            utc_time = pytz.utc.localize(utc_time)
            local_tz = pytz.timezone(timezone)
            local_time = utc_time.astimezone(local_tz)

            # Preparando o dicionário com os dados formatados
            time_data = {
                'year': local_time.year,
                'month': local_time.month,
                'day': local_time.day,
                'hour': local_time.hour,
                'minute': local_time.minute,
                'seconds': local_time.second,
                'milliSeconds': local_time.microsecond // 1000,  # Convertendo microssegundos para milissegundos
                'timeZone': timezone
            }

            return time_data
        
        return None
    except requests.exceptions.RequestException as e:
        return None
def fetch_httpbin():
    global httpbin
    httpbin = get_time_from_httpbin("America/Sao_Paulo")

# converter para aware
def Jsondate_to_datetime(timeapi):
        
        naive = datetime(2020, 1, 1, 0, 0, 0)

        tzinfo=pytz.timezone(timeapi["timeZone"]).localize(naive)

        naive  = datetime(
            timeapi["year"],
            timeapi["month"],
            timeapi["day"], 
            timeapi["hour"], 
            timeapi["minute"],
            timeapi["seconds"],
            timeapi["milliSeconds"], 
        )

        aware = pytz.timezone('America/Sao_Paulo').localize(naive)
        return aware

#calcular média
def average_datetimes_milliseconds(datetimes):
    if not datetimes:
        return None

    # Converter datetimes para timestamps em milissegundos
    timestamps_ms = [dt.timestamp() * 1000 for dt in datetimes]

    # Calcular a média dos timestamps
    avg_timestamp_ms = sum(timestamps_ms) / len(timestamps_ms)

    # Converter a média de volta para datetime (em milissegundos)
    avg_datetime = datetime.fromtimestamp(avg_timestamp_ms / 1000, pytz.timezone('America/Sao_Paulo'))

    return avg_datetime

def getamount():
    global timeapi
    global httpbin
    thread1 = threading.Thread(target=fetch_timeapi)
    thread2 = threading.Thread(target=fetch_httpbin)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()



    datetimes = [get_local_datetime()]

    if timeapi != None:
        datetimes.append(Jsondate_to_datetime(timeapi))

    if httpbin != None:
        datetimes.append(Jsondate_to_datetime(httpbin))

    if len(datetimes) > 1:
        return average_datetimes_milliseconds(datetimes)

    return (datetimes[0])

def getAmount():
    amount = getamount()
    return time.mktime(amount.timetuple()) + amount.microsecond / 1E6


if __name__ == "__main__":

    print(getamount())
'''
'''

