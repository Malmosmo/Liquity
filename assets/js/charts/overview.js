if (document.getElementById("charts") != null) {
    let url = document.getElementById("charts").getAttribute("url")

    fetch(url).then(response => {
        return response.json()
    }).then(json => {
        let max = 5

        // Chart 1
        {
            let series = json.data.map(({ _, date, count }) => ([new Date(date), count]))

            json.data.reduce((_, current) => {
                max = Math.max(max, current.count)
            })

            var options = {
                series: [{
                    name: "Drinks",
                    data: series
                }],
                title: {
                    text: "Drinks",
                    align: "left",
                },
                subtitle: {
                    text: "just Drinks",
                    align: "left",
                },
                chart: {
                    fontFamily: 'system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","Liberation Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
                    id: 'area-datetime',
                    type: 'area',
                    height: 350,
                    zoom: {
                        autoScaleYaxis: true
                    }
                },
                stroke: {
                    curve: 'straight'
                },
                dataLabels: {
                    enabled: false
                },
                markers: {
                    size: 0,
                    style: 'hollow',
                },
                yaxis: {
                    min: 0,
                    max: max + 1,
                    tickAmount: max,
                },
                xaxis: {
                    type: 'datetime',
                    tickAmount: 10,
                },
                tooltip: {
                    x: {
                        format: 'dd.MM.yy - HH:mm'
                    },
                },
                fill: {
                    type: 'gradient',
                    gradient: {
                        shadeIntensity: 1,
                        opacityFrom: 0.7,
                        opacityTo: 0.9,
                        stops: [0, 100]
                    }
                },
            };

            var chartTimeline = new ApexCharts(document.querySelector("#chart-timeline"), options);
            chartTimeline.render();

            // event listeners for chart 1
            document.querySelector('#one_year').addEventListener('click', () => {
                chartTimeline.zoomX(
                    new Date('1 Jan 2021').getTime(),
                    new Date('1 Jan 2022').getTime()
                )
            })

            document.querySelector('#one_month').addEventListener('click', () => {
                chartTimeline.zoomX(
                    new Date('1 Dec 2021').getTime(),
                    new Date('31 Dec 2021').getTime()
                )
            })

            document.querySelector('#all').addEventListener('click', () => {
                chartTimeline.zoomX(
                    undefined,
                    undefined
                )
            })
        }

        // Chart 2
        {
            let types = {}
            let series = []

            for (const entry of json.data) {
                if (entry.beer in types) {
                    types[entry.beer].push({
                        x: new Date(entry.date),
                        y: entry.count
                    })
                } else {
                    types[entry.beer] = [{
                        x: new Date(entry.date),
                        y: entry.count
                    }]
                }
            }

            for (const [key, value] of Object.entries(types)) {
                series.push({
                    name: key,
                    data: value
                })
            }

            var options = {
                series: series,
                chart: {
                    fontFamily: 'system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","Liberation Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"',
                    type: 'bar',
                    height: 350,
                    zoom: {
                        autoScaleYaxis: true
                    }
                },
                title: {
                    text: "Drinks",
                    align: "left",
                },
                subtitle: {
                    text: "by Type",
                    align: "left",
                },
                plotOptions: {
                    bar: {
                        horizontal: false,
                        columnWidth: '55%',
                        endingShape: 'rounded',
                    },
                },
                dataLabels: {
                    enabled: false
                },
                yaxis: {
                    min: 0,
                    max: max + 1,
                    tickAmount: max,
                },
                xaxis: {
                    type: 'datetime',
                    tickAmount: 10,
                },
                theme: {
                    mode: 'light',
                    palette: 'palette4',
                    monochrome: {
                        enabled: false,
                        color: '#255aee',
                        shadeTo: 'light',
                        shadeIntensity: 0.65
                    },
                },
                tooltip: {
                    x: {
                        format: 'dd.MM.yy - HH:mm'
                    },
                }
            };

            var chart = new ApexCharts(document.querySelector("#chart-type"), options);
            chart.render();
        }

        // Chart 3
        {
            let types = {}

            for (const entry of json.data) {
                if (entry.beer in types) {
                    types[entry.beer] += entry.count
                } else {
                    types[entry.beer] = entry.count
                }
            }

            var options = {
                series: Object.values(types),
                chart: {
                    type: 'donut',
                    toolbar: {
                        show: true,
                        offsetX: 0,
                        offsetY: 0,
                        tools: {
                            download: true,
                        }
                    }
                },
                title: {
                    text: "Drinks",
                    align: "left",
                },
                legend: {
                    show: false
                },
                subtitle: {
                    text: "by Type",
                    align: "left",
                },
                labels: Object.keys(types),
                dataLabels: {
                    offset: 0,
                    minAngleToShowLabel: 10
                },
                plotOptions: {
                    pie: {
                        customScale: 1.0,
                        donut: {
                            labels: {
                                show: true,
                                name: {
                                    show: true,
                                    fontSize: "22px"
                                }
                            }
                        }
                    },
                },

            };

            var chart = new ApexCharts(document.querySelector("#chart-pie"), options);
            chart.render();
        }
    })

}
