<template>
    <div class="network">
        <h1>Network component</h1>
        <div id="d3-el"></div>
    </div>
</template>

<script>
    export default {
        name: "network",
        mounted() {
            run_d3(this.$store.state.subnetwork.nodes, this.$store.state.subnetwork.links)
        }
    }

function run_d3() {
    const width = 640,
          height = 480;

    const nodes = [
        { x:   width/3, y: height/2 },
        { x: 2*width/3, y: height/2 }
    ];

    const links = [
        { source: 0, target: 1 }
    ];

    const svg = d3.select('#d3-el').append('svg')
        .attr('width', width)
        .attr('height', height);

    const force = d3.layout.force()
        .size([width, height])
        .nodes(nodes)
        .links(links)

    force.linkDistance(width/2);

    const link = svg.selectAll('.link')
        .data(links)
        .enter().append('line')
        .attr('class', 'link');

    const node = svg.selectAll('.node')
        .data(nodes)
        .enter().append('circle')
        .attr('class', 'node');

    force.on('end', function() {
        node.attr('r', width/25)
            .attr('cx', function(d) { return d.x; })
            .attr('cy', function(d) { return d.y; });

        link.attr('x1', function(d) { return d.source.x; })
            .attr('y1', function(d) { return d.source.y; })
            .attr('x2', function(d) { return d.target.x; })
            .attr('y2', function(d) { return d.target.y; });
    });

    force.start();
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