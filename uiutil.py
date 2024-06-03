def get_south_y(y_size_pixels:int, north_y:float):
    return (y_size_pixels/1080)+north_y

def calc_dist2(south_y):
    return south_y+((0.95-south_y)/2)

def calc_dist3(south_y):
    return south_y+((0.95-south_y)/3)

def calc_dist23(south_y):
    return south_y+((2*(0.95-south_y))/3)

def determine_month(month:str) -> str:
    months = {"": "00", "January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06", "July":"07", "August":"08", "September":"09", "October":"10", "November":"11", "December":"12"}
    return months[month]

def determine_day(day:str) -> str:
    days = {"": "00", '1st':"01", '2nd':"02", '3rd':"03", '4th':"04", '5th':"05", '6th':"06", '7th':"07", '8th':"08", '9th':"09", '10th':"10", '11th':"11", '12th':"12", '13th':"13", '14th':"14", '15th':"15", '16th':"16", '17th':"17", '18th':"18", '19th':"19", '20th':"20", '21st':"21", '22nd':"22", '23rd':"23", '24th':"24", '25th':"25", '26th':"26", '27th':"27", '28th':"28", '29th':"29", '30th':"30", '31st':"31"}
    return days[day]