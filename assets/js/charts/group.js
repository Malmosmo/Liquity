if (document.getElementById("group-charts") != null) {
    let url = document.getElementById("group-charts").getAttribute("url")

    fetch(url).then(response => {
        return response.json()
    }).then(json => {
        // let series = []
        // let max = 5

        // for (const entry of json.data.data) {
        //     if (entry.drinks.length > 0) {
        //         entry.drinks.reduce((_, current) => {
        //             max = Math.max(max, current.count)
        //         })
        //     }

        //     series.push({
        //         name: entry.name,
        //         data: entry.drinks.map(({ _, date, count }) => ([new Date(date), count]))
        //     })
        // }

        // Chart 1
        {
            // console.log(json.data)

            // series = []

            // for (const member of json.data.data) {
            //     let OBJ = {}

            //     for (const data of member.drinks) {
            //         let date = new Date(new Date(data.date).toDateString())

            //         // date.setDate(0)

            //         if (date in OBJ) {
            //             OBJ[date] += data.count
            //         } else {
            //             OBJ[date] = data.count
            //         }
            //     }

            //     let dd = []

            //     for (const [key, value] of Object.entries(OBJ)) {
            //         dd.push({
            //             x: key,
            //             y: value
            //         })
            //     }
            //     entry = {
            //         name: member.name,
            //         data: dd
            //     }
            //     series.push(entry)
            // }

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

                    array.push({
                        x: new Date(date1.toDateString()),
                        y: (sum / n).toFixed(2)
                    })
                }

                return array
            }

            let series = []

            for (const member of json.data.data) {
                series.push({
                    name: member.name,
                    data: getNDayMean(cleanUpData(member.drinks), 7),
                    // color: "#" + ((1 << 24) * Math.random() | 0).toString(16)
                })
            }

            var options = {
                series: series,
                chart: {
                    fontFamily: 'system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","Liberation Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
                    id: 'area-datetime',
                    type: 'area',
                    height: 350,
                    zoom: {
                        autoScaleYaxis: true
                    },
                    // zoom: {
                    //     enabled: false
                    // },
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

            var chart = new ApexCharts(document.querySelector("#line-chart"), options);
            chart.render();
        }
        // Chart 2
        // {
        //     var options = {
        //         series: series,
        //         chart: {
        //             fontFamily: 'system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","Liberation Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
        //             type: 'bar',
        //             height: 350,
        //             zoom: {
        //                 autoScaleYaxis: true
        //             }
        //         },
        //         title: {
        //             text: "Drinks",
        //             align: "left",
        //         },
        //         subtitle: {
        //             text: "by Type",
        //             align: "left",
        //         },
        //         plotOptions: {
        //             bar: {
        //                 horizontal: false,
        //                 columnWidth: '55%',
        //                 endingShape: 'rounded',
        //             },
        //         },
        //         dataLabels: {
        //             enabled: false
        //         },
        //         yaxis: {
        //             min: 0,
        //             max: max + 1,
        //             tickAmount: max,
        //         },
        //         xaxis: {
        //             type: 'datetime',
        //             tickAmount: 10,
        //         },
        //         theme: {
        //             mode: 'light',
        //             palette: 'palette4',
        //             monochrome: {
        //                 enabled: false,
        //                 color: '#255aee',
        //                 shadeTo: 'light',
        //                 shadeIntensity: 0.65
        //             },
        //         },
        //         tooltip: {
        //             x: {
        //                 format: 'dd.MM.yy - HH:mm'
        //             },
        //         }
        //     };

        //     var chart = new ApexCharts(document.querySelector("#bar-chart"), options);
        //     chart.render();
        // }
    })

}
