users = [
                {
                    'user_email' : 'bbbbbb@example.com',
                    'password'   :  'pass',
                    'travel_history' :[
                                        {
                                            'date' : '2020-03-01',
                                            'time' : '13-15',
                                            'location' : '10.5276N, 76.2144E'
                                        }
                                    ]
                },
                {
                    'user_email' : 'cccccc@world.com',
                    'password'   :  'pass',
                    'travel_history' :[
                                        {
                                            'date' : '2020-03-01',
                                            'time' : '15-00',
                                            'location' : '10.5221N, 76.2237E'
                                        }
                                    ]
                },
                {
                    'user_email' : 'dddddd@china.com',
                    'password'   :  'pass',
                    'travel_history' :[
                                        {
                                            'date' : '2020-03-02',
                                            'time' : '17-30',
                                            'location' : '19.2183N, 72.9781E'
                                        },
                                        {
                                            'date' : '2020-03-01',
                                            'time' : '17-25',
                                            'location' : '27.1751N, 78.0421E'
                                        }
                                    ]
                }
                
                
            ]
def userdetails():
    return users