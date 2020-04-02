# this is a temporary patient database working as dummy sql database

patients = [
                {
                    'patient_id' : 0,
                    'result' : 'negative',
                    'patient_email' : 'email@example.com',
                    'travel_history' :[
                                        {
                                            'date' : '2020-03-01',
                                            'time' : '01-15',
                                            'location' : '10.5276N, 76.2144E'
                                        }
                                    ]
                },
                {
                    'patient_id' : 1,
                    'result' : 'negative',
                    'patient_email' : 'corona@world.com',
                    'travel_history' :[
                                        {
                                            'date' : '2020-03-01',
                                            'time' : '15-00',
                                            'location' : '10.5221N, 76.2237E'
                                        }
                                    ]
                },
                {
                    'patient_id' : 2,
                    'result' : 'positive',
                    'patient_email' : 'cure@china.com',
                    'travel_history' :[
                                        {
                                            'date' : '2020-03-02',
                                            'time' : '17-30',
                                            'location' : '10.2544N, 76.3681E'
                                        }
                                    ]
                },
                {
                    'patient_id' : 3,
                    'result' : 'positive',
                    'patient_email' : 'india@lockdown.com',
                    'travel_history' :[
                                        {
                                            'date' : '2020-03-01',
                                            'time' : '11-00',
                                            'location' : '19.0760N, 72.8777E'
                                        },
                                        {
                                            'date' : '2020-03-02',
                                            'time' : '11-45',
                                            'location' : '19.0760N, 72.8777E'
                                        },
                                        {
                                            'date' : '2020-03-02',
                                            'time' : '18-10',
                                            'location' : '19.2183N, 72.9781E'
                                        }
                                    ]
                },
                {
                    'patient_id' : 4,
                    'result' : 'negative',
                    'patient_email' : 'italy@paralokam.com',
                    'travel_history' :[
                                        {
                                            'date' : '2020-03-01',
                                            'time' : '17-00',
                                            'location' : '28.7041N, 77.1025E'
                                        },
                                        {
                                            'date' : '2020-03-01',
                                            'time' : '19-25',
                                            'location' : '27.1751N, 78.0421E'
                                        }
                                    ]
                },
                {
                    'patient_id' : 5,
                    'result' : 'negative',
                    'patient_email' : 'me@home.com',
                    'travel_history' :[
                                        {
                                            'date' : '2020-03-02',
                                            'time' : '08-00',
                                            'location' : '9.9312N, 76.2673E'
                                        }
                                    ]
                }
            ]
def database():
    return patients