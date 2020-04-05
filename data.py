# this is a temporary patient database working as dummy sql database

patients = [
            {
                'date' : '2020-03-01',
                'time' : '01-15',
                'latitude' : '10.5206N',
                'longitude' : '76.2140E'
            },
            {   'date' : '2020-03-01',
                'time' : '15-00',
                'latitude' : '10.5206N',
                'longitude' : '76.2140E'
            },
            {
                'date' : '2020-03-02',
                'time' : '17-30',
                'latitude' : '10.5206N',
                'longitude' : '76.2140E'
            },
            {
                'date' : '2020-03-01',
                'time' : '11-00',
                'latitude' : '10.5206N',
                'longitude' : '76.2140E'
            },
            {
                'date' : '2020-03-02',
                'time' : '11-45',
                'latitude' : '10.5206N',
                'longitude' : '76.2140E'
            },
            {
                'date' : '2020-03-02',
                'time' : '18-10',
                'latitude' : '10.5206N',
                'longitude' : '76.2140E'
            }
                                    ]

def database():
    return patients