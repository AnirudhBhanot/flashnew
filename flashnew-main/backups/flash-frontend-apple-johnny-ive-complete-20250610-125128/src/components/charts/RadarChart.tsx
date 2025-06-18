import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import styles from './RadarChart.module.scss';

interface RadarChartProps {
  data: {
    axis: string;
    value: number;
    fullName?: string;
  }[];
  size?: number;
  levels?: number;
  maxValue?: number;
}

export const RadarChart: React.FC<RadarChartProps> = ({
  data,
  size = 400,
  levels = 5,
  maxValue = 1
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  
  useEffect(() => {
    if (!svgRef.current || !data.length) return;
    
    // Clear previous chart
    d3.select(svgRef.current).selectAll('*').remove();
    
    const margin = 80;
    const radius = (size - 2 * margin) / 2;
    const angleSlice = (Math.PI * 2) / data.length;
    
    // Create SVG
    const svg = d3.select(svgRef.current)
      .attr('width', size)
      .attr('height', size);
    
    const g = svg.append('g')
      .attr('transform', `translate(${size / 2}, ${size / 2})`);
    
    // Draw circular grid
    const axisGrid = g.append('g').attr('class', styles.axisGrid);
    
    // Circles
    const gridCircles = d3.range(1, levels + 1).reverse();
    
    axisGrid.selectAll('.gridCircle')
      .data(gridCircles)
      .enter()
      .append('circle')
      .attr('class', styles.gridCircle)
      .attr('r', d => radius / levels * d)
      .attr('fill', 'none')
      .attr('stroke', 'var(--border-color)')
      .attr('stroke-width', 1);
    
    // Grid labels
    axisGrid.selectAll('.gridLabel')
      .data(gridCircles)
      .enter()
      .append('text')
      .attr('class', styles.gridLabel)
      .attr('x', 4)
      .attr('y', d => -radius / levels * d)
      .attr('dy', '0.4em')
      .text(d => `${Math.round((maxValue * d) / levels * 100)}%`)
      .attr('fill', 'var(--text-secondary)')
      .attr('font-size', '12px');
    
    // Axis lines
    const axis = axisGrid.selectAll('.axis')
      .data(data)
      .enter()
      .append('g')
      .attr('class', styles.axis);
    
    axis.append('line')
      .attr('x1', 0)
      .attr('y1', 0)
      .attr('x2', (d, i) => radius * Math.cos(angleSlice * i - Math.PI / 2))
      .attr('y2', (d, i) => radius * Math.sin(angleSlice * i - Math.PI / 2))
      .attr('stroke', 'var(--border-color)')
      .attr('stroke-width', 1);
    
    // Axis labels
    axis.append('text')
      .attr('class', styles.axisLabel)
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('x', (d, i) => (radius + 20) * Math.cos(angleSlice * i - Math.PI / 2))
      .attr('y', (d, i) => (radius + 20) * Math.sin(angleSlice * i - Math.PI / 2))
      .text(d => d.axis)
      .attr('fill', 'var(--text-primary)')
      .attr('font-size', '14px')
      .attr('font-weight', '500');
    
    // Line function
    const radarLine = d3.lineRadial<{ axis: string; value: number }>()
      .radius(d => radius * (d.value / maxValue))
      .angle((d, i) => i * angleSlice)
      .curve(d3.curveLinearClosed);
    
    // Data area
    const dataArea = g.append('g').attr('class', styles.dataArea);
    
    // Fill area
    dataArea.append('path')
      .datum(data)
      .attr('class', styles.radarArea)
      .attr('d', radarLine as any)
      .attr('fill', 'var(--color-primary)')
      .attr('fill-opacity', 0.2)
      .attr('stroke', 'var(--color-primary)')
      .attr('stroke-width', 2);
    
    // Data points
    dataArea.selectAll('.radarCircle')
      .data(data)
      .enter()
      .append('circle')
      .attr('class', styles.radarCircle)
      .attr('r', 4)
      .attr('cx', (d, i) => radius * (d.value / maxValue) * Math.cos(angleSlice * i - Math.PI / 2))
      .attr('cy', (d, i) => radius * (d.value / maxValue) * Math.sin(angleSlice * i - Math.PI / 2))
      .attr('fill', 'var(--color-primary)')
      .attr('stroke', '#fff')
      .attr('stroke-width', 2);
    
    // Tooltip
    const tooltip = d3.select('body').append('div')
      .attr('class', styles.tooltip)
      .style('opacity', 0);
    
    dataArea.selectAll('.radarCircle')
      .on('mouseover', function(event, d: any) {
        tooltip.transition()
          .duration(200)
          .style('opacity', 0.9);
        tooltip.html(`
          <div>${d.fullName || d.axis}</div>
          <div>${Math.round(d.value * 100)}%</div>
        `)
          .style('left', (event.pageX + 10) + 'px')
          .style('top', (event.pageY - 28) + 'px');
      })
      .on('mouseout', function() {
        tooltip.transition()
          .duration(500)
          .style('opacity', 0);
      });
    
    // Cleanup
    return () => {
      d3.select('body').selectAll(`.${styles.tooltip}`).remove();
    };
  }, [data, size, levels, maxValue]);
  
  return (
    <div className={styles.container}>
      <svg ref={svgRef} />
    </div>
  );
};

export default RadarChart;