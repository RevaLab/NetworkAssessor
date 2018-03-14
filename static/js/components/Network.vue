<template>
    <div class="network">
        <h1>Network component</h1>
        <div v-if="isReady">
            <div id="d3-el"></div>
        </div>
        <div v-else>Loading...</div>
    </div>
</template>

<script>
    export default {
        name: "network",
        data() {
            return {}
        },
        computed: {
            isReady() { return this.$store.state.subnetwork }
        },
        watch: {
            isReady() { run_d3(this.$store.state.subnetwork) }
        },
    }

    function run_d3(graph) {
        const edges = [];

        graph.links.forEach(function (e) {
            const sourceNode = graph.nodes.filter(function (n) {
                    return n.id === e.source;
                })[0],
                targetNode = graph.nodes.filter(function (n) {
                    return n.id === e.target;
                })[0];

            edges.push({source: sourceNode, target: targetNode});
        });

        graph.links = edges;

        let w = 1000;
        let h = 1000;

        // let keyc = true, keys = true, keyt = true, keyr = true, keyx = true, keyd = true, keyl = true, keym = true,
        //     keyh = true, key1 = true, key2 = true, key3 = true, key0 = true
        let focus_node = null, highlight_node = null;

        let text_center = false;
        let outline = false;

        let highlight_color = "blue";
        let highlight_trans = 0.1;

        let size = d3.scale.pow().exponent(1)
            .domain([1, 100])
            .range([8, 24]);

        let force = d3.layout.force()
            .linkDistance(60)
            .charge(-2000)
            .size([w, h]);

        let default_node_color = "#ccc";
        let default_link_color = "#b0b0b0";
        let nominal_base_node_size = 8;
        let nominal_text_size = 10;
        let max_text_size = 24;
        let nominal_stroke = 1.5;
        let max_stroke = 4.5;
        let max_base_node_size = 36;
        let min_zoom = 0.1;
        let max_zoom = 7;

        let svg = d3.select("#d3-el").append("svg");
        let zoom = d3.behavior.zoom().scaleExtent([min_zoom, max_zoom]);
        let g = svg.append("g");
        svg.style("cursor", "move");

        let linkedByIndex = {};
        graph.links.forEach(function (d) {
            linkedByIndex[d.source + "," + d.target] = true;
        });

        function isConnected(a, b) {
            return linkedByIndex[a.index + "," + b.index] ||
                linkedByIndex[b.index + "," + a.index] ||
                a.index === b.index;
        }

        function hasConnections(a) {
            for (let property in linkedByIndex) {
                s = property.split(",");
                if ((s[0] === a.index || s[1] === a.index) && linkedByIndex[property]) {
                    return true;
                }
            }
            return false;
        }

        force
            .nodes(graph.nodes)
            .links(graph.links)
            .start();

        const link = g.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link")
            .style("stroke-width", nominal_stroke)
            .style('stroke', default_link_color);
        // .style("stroke", function(d) {
        // if (isNumber(d.score) && d.score>=0) return color(d.score);
        // else return default_link_color; })

        const node = g.selectAll(".node")
            .data(graph.nodes)
            .enter().append("g")
            .attr("class", "node")

            .call(force.drag)

        node.on(
            "dblclick.zoom",
            function (d) {
                d3.event.stopPropagation();
                const dcx = (window.innerWidth / 2 - d.x * zoom.scale());
                const dcy = (window.innerHeight / 2 - d.y * zoom.scale());
                zoom.translate([dcx, dcy]);
                g.attr("transform", "translate(" + dcx + "," + dcy + ")scale(" + zoom.scale() + ")");
            }
        );

        let tocolor = "fill";
        let towhite = "stroke";
        if (outline) {
            tocolor = "stroke"
            towhite = "fill"
        }

        let circle = node.append("path")
            .attr("d", d3.svg.symbol()
                .size(function (d) {
                    return Math.PI * Math.pow(nominal_base_node_size, 2);
                })
                .type(function (d) {
                    return "circle";
                }))
            .attr("class", function(d) {
                if (d["queryList"]) {
                    return 'queryList'
                }
            })

            .style(tocolor, function (d) {
                return default_node_color;
            })
            .style("stroke-width", nominal_stroke)
            .style(towhite, "white");

        let text = g.selectAll(".text")
            .data(graph.nodes)
            .enter().append("text")
            .attr("dy", ".35em")
            .style("font-size", nominal_text_size + "px");

        if (text_center) {
            text.text(function (d) {
                return d.id;
            })
                .style("text-anchor", "middle");
        } else {
            text.attr("dx", function (d) {
                return nominal_base_node_size;
            })
                .text(function (d) {
                    return '\u2002' + d.id;
                });
        }

        node
            .on("mouseover", function (d) {
                set_highlight(d);
            })
            .on("mousedown",
                function (d) {
                    d3.event.stopPropagation();
                    focus_node = d;

                    if (highlight_node === null) {
                        set_highlight(d)
                    }
                })
            .on("mouseout", function (d) {
                exit_highlight();
            });

        d3.select(window).on("mouseup",
            function () {
                if (focus_node !== null) {
                    focus_node = null;
                    if (highlight_trans < 1) {
                        circle.style("opacity", 1);
                        text.style("opacity", 1);
                        link.style("opacity", 1);
                    }
                }

                if (highlight_node === null) {
                    exit_highlight();
                }
            }
        );

        function exit_highlight() {
            highlight_node = null;
            if (focus_node === null) {
                svg.style("cursor", "move");
                if (highlight_color !== "white") {
                    circle.style(towhite, "white");
                    text.style("font-weight", "normal");
                    link.style("stroke", function (o) {
                        return default_link_color;
                    });
                }

            }
        }


        function set_highlight(d) {
            svg.style("cursor", "pointer");
            if (focus_node !== null) {
                d = focus_node;
            }
            highlight_node = d;

            if (highlight_color !== "white") {
                circle.style(towhite, function (o) {
                    return isConnected(d, o) ? highlight_color : "white";
                });
                text.style("font-weight", function (o) {
                    return isConnected(d, o) ? "bold" : "normal";
                });
                link.style("stroke", function (o) {
                    return o.source.index === d.index ||
                    o.target.index === d.index ?
                        highlight_color : default_link_color;
                });
            }
        }

        zoom.on("zoom", function () {
            let stroke = nominal_stroke;
            if (nominal_stroke * zoom.scale() > max_stroke) {
                stroke = max_stroke / zoom.scale();
            }
            link.style("stroke-width", stroke);
            circle.style("stroke-width", stroke);

            let base_radius = nominal_base_node_size;
            if (nominal_base_node_size * zoom.scale() > max_base_node_size) base_radius = max_base_node_size / zoom.scale();
            circle.attr("d", d3.svg.symbol()
                .size(function (d) {
                    return Math.PI * Math.pow(size(d.size) * base_radius / nominal_base_node_size || base_radius, 2);
                })
                .type(function (d) {
                    return d.type;
                }))

            if (!text_center) text.attr("dx", function (d) {
                return (size(d.size) * base_radius / nominal_base_node_size || base_radius);
            });

            let text_size = nominal_text_size;
            if (nominal_text_size * zoom.scale() > max_text_size) {
                text_size = max_text_size / zoom.scale();
            }
            text.style("font-size", text_size + "px");
            g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        });

        svg.call(zoom);

        resize();

        d3.select(window).on("resize", resize)
            // .on("keydown", keydown);

        force.on("tick", function () {
            node.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
            text.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });

            link.attr("x1", function (d) {
                return d.source.x;
            })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });

            node.attr("cx", function (d) {
                return d.x;
            })
                .attr("cy", function (d) {
                    return d.y;
                });
        });

        function resize() {
            const width = window.innerWidth;
            const height = window.innerHeight;
            svg.attr("width", width).attr("height", height);

            force.size([force.size()[0] + (width - w) / zoom.scale(), force.size()[1] + (height - h) / zoom.scale()]).resume();
            w = width;
            h = height;
        }

        // function keydown() {
        //     if (d3.event.keyCode == 32) {
        //         force.stop();
        //     }
        //     else if (d3.event.keyCode >= 48 && d3.event.keyCode <= 90 && !d3.event.ctrlKey && !d3.event.altKey && !d3.event.metaKey) {
        //         switch (String.fromCharCode(d3.event.keyCode)) {
        //             case "C": keyc = !keyc; break;
        //             case "S": keys = !keys; break;
        //             case "T": keyt = !keyt; break;
        //             case "R": keyr = !keyr; break;
        //             case "X": keyx = !keyx; break;
        //             case "D": keyd = !keyd; break;
        //             case "L": keyl = !keyl; break;
        //             case "M": keym = !keym; break;
        //             case "H": keyh = !keyh; break;
        //             case "1": key1 = !key1; break;
        //             case "2": key2 = !key2; break;
        //             case "3": key3 = !key3; break;
        //             case "0": key0 = !key0; break;
        //         }
        //     }
        //
        //     link.style("display", function(d) {
        //         let flag = vis_by_type(d.source.type) && vis_by_type(d.target.type) && vis_by_node_score(d.source.score)&&vis_by_node_score(d.target.score)&&vis_by_link_score(d.score);
        //             linkedByIndex[d.source.index + "," + d.target.index] = flag;
        //           return flag?"inline":"none";
        //     });
        //
        //     node.style("display", function(d) {
        //         return (key0||hasConnections(d))&&vis_by_type(d.type)&&vis_by_node_score(d.score)?"inline":"none";
        //     });
        //
        //     text.style("display", function(d) {
        //         return (key0||hasConnections(d))&&vis_by_type(d.type)&&vis_by_node_score(d.score)?"inline":"none";
        //     });
        //
        //     if (highlight_node !== null) {
        //         if ((key0||hasConnections(highlight_node))&&vis_by_type(highlight_node.type)&&vis_by_node_score(highlight_node.score)) {
        //             if (focus_node!==null) set_focus(focus_node);
        //             set_highlight(highlight_node);
        //         } else { exit_highlight(); }
        //     }
        // }


    }


</script>

<style>
    .node {
        fill: #ccc;
        stroke: #fff;
        stroke-width: 2px;
    }

    .link {
        stroke: #777;
        stroke-width: 2px;
    }
</style>