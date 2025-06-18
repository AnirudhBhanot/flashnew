import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import styles from './RadarChart.module.scss';

interface DataSeries {
  name: string;
  values: Record<string, number>;
}

interface MultiSeriesRadarChartProps {
  data: DataSeries[];
  size?: number;
  levels?: number;
  maxValue?: number;
}

export const MultiSeriesRadarChart: React.FC<MultiSeriesRadarChartProps> = ({
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
    
    // Extract axes from first series
    const axes = Object.keys(data[0].values);
    const margin = 80;
    const radius = (size - 2 * margin) / 2;
    const angleSlice = (Math.PI * 2) / axes.length;
    
    // Color scale
    const color = d3.scaleOrdinal()
      .domain(data.map(d => d.name))
      .range(['#007AFF', '#FF9500', '#34C759', '#AF52DE']);
    
    // Create SVG
    const svg = d3.select(svgRef.current)
      .attr('width', size)
      .attr('height', size);
    
    const g = svg.append('g')
      .attr('transform', `translate(${size / 2}, ${size / 2})`);
    
    // Grid
    const axisGrid = g.append('g').attr('class', styles.axisGrid);
    
    // Circular grid
    const gridCircles = d3.range(1, levels + 1).map(level => level);
    
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
      .data(axes)
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
      .text(d => d)
      .attr('fill', 'var(--text-primary)')
      .attr('font-size', '14px')
      .attr('font-weight', '500');
    
    // Line function
    const radarLine = d3.lineRadial<[number, number]>()
      .curve(d3.curveLinearClosed);
    
    // Data area for each series
    const dataArea = g.append('g').attr('class', styles.dataArea);
    
    data.forEach((series, seriesIndex) => {
      const seriesData = axes.map((axis, i) => {
        const angle = i * angleSlice;
        const value = series.values[axis] || 0;
        return [angle, radius * (value / maxValue)] as [number, number];
      });
      
      // Fill area
      dataArea.append('path')
        .datum(seriesData)
        .attr('class', `${styles.radarArea} radar-area-${seriesIndex}`)
        .attr('d', radarLine)
        .attr('fill', color(series.name) as string)
        .attr('fill-opacity', 0.1)
        .attr('stroke', color(series.name) as string)
        .attr('stroke-width', 2);
      
      // Data points
      seriesData.forEach(([angle, r], i) => {
        const x = r * Math.cos(angle - Math.PI / 2);
        const y = r * Math.sin(angle - Math.PI / 2);
        
        dataArea.append('circle')
          .attr('class', styles.radarCircle)
          .attr('r', 4)
          .attr('cx', x)
          .attr('cy', y)
          .attr('fill', color(series.name) as string)
          .attr('stroke', '#fff')
          .attr('stroke-width', 2)
          .on('mouseover', function(event) {
            // Show tooltip
            const tooltip = d3.select('body').append('div')
              .attr('class', styles.tooltip)
              .style('opacity', 0);
            
            tooltip.transition()
              .duration(200)
              .style('opacity', 0.9);
            tooltip.html(`
              <div><strong>${series.name}</strong></div>
              <div>${axes[i]}: ${Math.round(series.values[axes[i]] * 100)}%</div>
            `)
              .style('left', (event.pageX + 10) + 'px')
              .style('top', (event.pageY - 28) + 'px');
          })
          .on('mouseout', function() {
            d3.selectAll(`.${styles.tooltip}`).remove();
          });
      });
    });
    
    // Cleanup on unmount
    return () => {
      d3.selectAll(`.${styles.tooltip}`).remove();
    };
  }, [data, size, levels, maxValue]);
  
  return (
    <div className={styles.container}>
      <svg ref={svgRef} />
    </div>
  );
};