if (document.getElementById("charts") != null) {
    let url = document.getElementById("charts").getAttribute("url")
    console.log(url)
    fetch(url).then(response => {
        return response.json()
    }).then(json => {
        // Chart 1
        {
            // Note: List has to be sorted
            // Note: n > 0
            function cleanUpData(list) {
                let dict = {}

                for (const entry of list) {
                    let date = new Date(new Date(entry.date).toDateString())

                    if (date in dict) {
                        dict[date] += entry.count * entry.volume
                    } else {
                        dict[date] = entry.count * entry.volume
                    }
                }

                let result = []

                for (const [key, value] of Object.entries(dict)) {
                    result.push({
                        date: key,
                        count: value
                    })
                }

                return result
            }

            function getNDayMean(list, n) {
                let array = []

                for (let i = 0; i < list.length; i++) {
                    let date1 = new Date(list[i].date)

                    let sum = 0

                    for (let j = i; j >= 0; j--) {
                        let date2 = new Date(list[j].date)

                        if (Math.abs(date1.getDate() - date2.getDate()) <= n) {
                            sum += list[j].count
                        } else {
                            break
                        }
                    }

                    date1.setHours(1)

                    array.push({
                        x: date1,
                        y: (sum / n).toFixed(2)
                    })
                }

                return array
            }

            var options = {
                series: [{
                    name: "Last 7 Day Average",
                    data: getNDayMean(cleanUpData(json.data), 7)
                }],
                // title: {
                //     text: "7 Day Average",
                //     align: "left",
                // },
                // subtitle: {
                //     text: "in Liters",
                //     align: "left",
                // },
                // noData: {
                //     text: "Empty"
                // },
                chart: {
                    fontFamily: 'system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","Liberation Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
                    id: 'area-datetime',
                    type: 'area',
                    height: 350,
                    // zoom: {
                    //     autoScaleYaxis: true
                    // },
                    zoom: {
                        enabled: false
                    },
                    toolbar: {
                        show: false
                    },
                    shadow: {
                        enabled: false,
                    }
                },
                stroke: {
                    // curve: 'straight'
                    curve: 'smooth',
                    // curve: 'stepline',
                    width: 4,
                },
                dataLabels: {
                    enabled: false
                },
                markers: {
                    size: 0,
                    style: 'hollow',
                },
                xaxis: {
                    type: 'datetime',
                    axisBorder: {
                        show: false
                    },
                    axisTicks: {
                        show: false
                    },
                    labels: {
                        style: {
                            colors: '#999',
                            // fontSize: '13px',
                            // fontFamily: '#333',
                            // cssClass: 'display-1',
                        }
                    },
                    tooltip: {
                        enabled: false
                    },
                    crosshairs: {
                        show: true,
                    }
                    // tickAmount: 5,
                },
                yaxis: {
                    min: 0,
                    // max: 10,
                    tickAmount: 5,
                    axisBorder: {
                        show: false
                    },
                    axisTicks: {
                        show: false
                    },
                    labels: {
                        style: {
                            colors: '#777',
                            // fontSize: '13px',
                            // fontFamily: '#333',
                            // cssClass: 'display-1',
                        }
                    }
                },
                grid: {
                    borderColor: '#f3f3f3',
                    strokeDashArray: 3,
                },
                tooltip: {
                    shared: true,
                    intersect: false,
                    x: {
                        // format: 'dd.MM.yy - HH:mm'
                        format: 'dd.MM.yy',
                    },
                    y: {
                        show: false,
                        formatter: (value) => (value + " Liters")
                    }
                },
                fill: {
                    type: 'gradient',
                    gradient: {
                        shadeIntensity: 1,
                        opacityFrom: 0.3,
                        opacityTo: 0.6,
                        stops: [0, 100]
                    }
                },
            };

            var chartTimeline = new ApexCharts(document.querySelector("#timeline-chart"), options);
            chartTimeline.render();

            // // event listeners for chart 1
            // document.querySelector('#one_year').addEventListener('click', () => {
            //     chartTimeline.zoomX(
            //         new Date('1 Jan 2021').getTime(),
            //         new Date('1 Jan 2022').getTime()
            //     )
            // })

            // document.querySelector('#one_month').addEventListener('click', () => {
            //     chartTimeline.zoomX(
            //         new Date('1 Dec 2021').getTime(),
            //         new Date('31 Dec 2021').getTime()
            //     )
            // })

            // document.querySelector('#all').addEventListener('click', () => {
            //     chartTimeline.zoomX(
            //         undefined,
            //         undefined
            //     )
            // })
        }

        // Chart 2
        {
            let types = {}

            for (const entry of json.data) {
                if (entry.beer in types) {
                    types[entry.beer] += entry.count * entry.volume
                } else {
                    types[entry.beer] = entry.count * entry.volume
                }
            }

            let array = []

            for (const key of Object.keys(types)) {
                array.push([key, types[key]])
            }

            array.sort((a, b) => { return b[1] - a[1] })

            let values = []
            let keys = []

            // top 10
            for (const [key, value] of array.slice(0, 10)) {
                values.push(value)
                keys.push(key)
            }

            /**
             * 
             * 
             * 
             */

            let tbody = document.querySelector("#tbody")
            let i = 1
            for (const element of array) {
                tbody.innerHTML += `
                    <tr>
                        <td>${i}</td>
                        <td>${element[0]}</td>
                        <td>${element[1].toFixed(2)}<sup>l</sup></td>
                    </tr>
                `
                i++;
            }

            // Get Top 10 Share
            // let totalShare = values.reduce((partialSum, a) => partialSum + a, 0)
            // let total = parseInt(document.querySelector("#total").innerText.replace(",", "."))

            // percentage = 0
            // if (total != 0) {
            //     percentage = (totalShare / total * 100).toFixed(0)
            // }
            // document.querySelector("#share").innerHTML = percentage + "<sup class='fs-6 fw-lighter'>%</sup>"

            var options = {
                series: values,
                chart: {
                    type: 'donut',
                    toolbar: {
                        show: false,
                        // offsetX: 0,
                        // offsetY: 0,
                        // tools: {
                        //     download: true,
                        // }
                    },
                    height: '600px'
                },
                // title: {
                //     text: "Your Top 10 Drinks",
                //     align: "left",
                // },
                legend: {
                    show: false
                },
                // subtitle: {
                //     text: "by Type",
                //     align: "left",
                // },
                labels: keys,
                dataLabels: {
                    offset: 0,
                    // minAngleToShowLabel: 10
                },
                tooltip: {
                    y: {
                        formatter: (value) => (parseFloat(value).toFixed(2) + " Liters")
                    }
                },
                plotOptions: {
                    pie: {
                        customScale: 1.0,
                        donut: {
                            labels: {
                                show: true,
                                name: {
                                    show: true,
                                    fontSize: "2rem",
                                    formatter: (name) => {
                                        if (name.length > 20) {
                                            return name.slice(0, 20) + "..."
                                        }
                                        return name
                                    }
                                },
                                value: {
                                    fontSize: "2rem",
                                    formatter: (value) => (parseFloat(value).toFixed(2) + " Liters")
                                },
                                total: {
                                    show: true,
                                    showAlways: false,
                                    label: 'Total',
                                    fontSize: '2rem',
                                    formatter: function (w) {
                                        return w.globals.seriesTotals.reduce((a, b) => {
                                            return a + b
                                        }, 0) + " Liters"
                                    }
                                }
                            }
                        }
                    },
                },
                responsive: [{
                    breakpoint: 800,
                    options: {
                        chart: {
                            height: "auto"
                        },
                        plotOptions: {
                            pie: {
                                customScale: 1.0,
                                donut: {
                                    labels: {
                                        name: {
                                            fontSize: "1.125rem",
                                            formatter: (name) => {
                                                if (name.length > 15) {
                                                    return name.slice(0, 15) + "..."
                                                }
                                                return name
                                            }
                                        },
                                        value: {
                                            fontSize: "1.125rem",
                                        },
                                        total: {
                                            fontSize: "1.125rem",
                                        }
                                    }
                                }
                            },
                        },
                    },
                }]
            };

            var chart = new ApexCharts(document.querySelector("#donut-chart"), options);
            chart.render();
        }

        // List
        let list_dict = sortByType(json.data)
        let list_array = Object.keys(list_dict).map(function (key) {
            return [key, list_dict[key]];
        })
        list_array.sort(function (first, second) {
            return second[1] - first[1];
        });

        console.log(list_array)

    })

}


function sortByType(data) {
    let dict = {}

    for (const entry of data) {
        if (entry.beer in dict) {
            dict[entry.beer] += entry.count * entry.volume
        } else {
            dict[entry.beer] = entry.count * entry.volume
        }
    }

    return dict
}