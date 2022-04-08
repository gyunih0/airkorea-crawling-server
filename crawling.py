import requests
from bs4 import BeautifulSoup
from timecode import setcode


areas = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기',
         '강원', '충북', '충남', '전북', '전남', '세종', '경북', '경남', '제주']
items = ['PM2.5', 'PM10']
area_code = {'서울': '02', '부산': '051', '대구': '053', '인천': '032',
             '광주': '062', '대전': '042', '울산': '052', '경기': '031', '강원': '033',
             '충북': '043', '충남': '041', '전북': '063', '전남': '061', '세종': '044',
             '경북': '054', '경남': '055', '제주': '064'}
item_code = {'PM2.5': '10008', 'PM10': '10007'}
data_name = ["측정소", "평균", "최대", "최소", "1시", "2시", "3시", "4시", "5시", "6시", "7시", "8시", "9시", "10시",
             "11시", "12시", "13시", "14시", "15시", "16시", "17시", "18시", "19시", "20시", "21시", "22시", "23시", "24시"]


def make_soup(area, item):
    """Get current time imformation and make a html soup"""
    codes = setcode()
    ymd = codes["ymd"]
    hour_code = codes["hour_code"]
    tdate = codes["tdate"]
    monthday = codes["monthday"]
    url = "https://www.airkorea.or.kr/web/sidoAirInfo/sidoAirInfoDay01?itemCode={}&ymd={}%{}&areaCode={}&tDate={}&monthDay={}".format(
        item_code[item], ymd, hour_code, area_code[area], tdate, monthday)

    res = requests.get(url)
    res.status_code

    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def combine(PM25, PM10, index):
    """combine concentration value of PM2.5 with that of PM10"""
    concentrations = {}

    concentration25 = PM25[index].text.strip()[:2]
    concentration10 = PM10[index].text.strip()[:2]
    concentrations['PM2.5'] = concentration25
    concentrations['PM10'] = concentration10

    return concentrations


def scrape(area, loc=None):
    """scrape values at the station or scrape all of them"""
    soup_pm25 = make_soup(area, 'PM2.5')
    soup_pm10 = make_soup(area, 'PM10')
    data_rows25 = soup_pm25.select('#board > table > tbody > tr')
    data_rows10 = soup_pm10.select('#board > table > tbody > tr')
    tdata = []  # double list for all data

    for i in range(len(data_rows25)):
        data = []  # A row data list

        column_name = data_rows25[i].select_one('th').text
        if column_name.startswith('['):  # to make city name refined
            column_name = column_name.split(']')[1]
        # print(column_name)

        if column_name == loc:  # scrape the location data
            data.append(column_name)
            concentrations25 = data_rows25[i].select('td')
            concentrations10 = data_rows10[i].select('td')

            for j in range(0, len(concentrations25)):  # combine data PM2.5 with PM10
                concentrations = combine(concentrations25, concentrations10, j)
                data.append(concentrations)

            return(data)

        else:  # scrape all location data
            data.append(column_name)
            concentrations25 = data_rows25[i].select('td')
            concentrations10 = data_rows10[i].select('td')

            for j in range(0, len(concentrations25)):  # combine data PM2.5 with PM10
                concentrations = combine(concentrations25, concentrations10, j)
                data.append(concentrations)

            tdata.append(data)
    return tdata


def scrape_one(area, loc, item):
    """scrape values of the one item """
    soup = make_soup(area, item)
    # Data extraction
    data_rows = soup.select('#board > table > tbody > tr')

    # Data refine
    for row in data_rows:
        data = []  # A row data list

        column_name = row.select_one('th').text
        if column_name.startswith('['):  # to make city name refined
            column_name = column_name.split(']')[1]

        if column_name == loc:
            data.append(column_name)

            concentrations = row.select('td')
            for concentration in concentrations:
                # Concentration text refine
                # Use slicing and strip
                tmp = concentration.text.strip()
                data.append(tmp[:2])
            print(data)
            return(data)
