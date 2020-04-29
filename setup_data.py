def setup_data(data):
    #print(data.head())
    data["Active"]=data["Confirmed"]-data["Recovered"]
    try:
        del data["Province/State"]
    except KeyError:
        del data["Province_State"]
    try:
        del data["Last_Update"]
    except KeyError:
        try:
            del data["Last Update"]
        except KeyError:
            s="l"
    try:
        del data["Long_"]
        del data["Lat"]
    except KeyError:
        s="l"
    try:
        del data["FIPS"]
    except KeyError:
        s="l"
    try:
        del data["Combined_Key"]
    except KeyError:
        s="l"
    #del data["Confirmed"]
    #del data["Deaths"]
    #del data["Recovered"]
    try:
        data=data.groupby("Country_Region").sum()
    except KeyError:
        data=data.groupby("Country/Region").sum()
    return data
