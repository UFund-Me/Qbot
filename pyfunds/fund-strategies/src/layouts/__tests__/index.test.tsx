import 'jest';
import BasicLayout from '..';
import React from 'react';
import renderer, { ReactTestInstance, ReactTestRenderer } from 'react-test-renderer';

describe('Layout: BasicLayout', () => {
  it('Render correctly', () => {
    const wrapper: ReactTestRenderer = renderer.create(<BasicLayout />);
    expect(wrapper.root.children.length).toBe(1);
    const outerLayer = wrapper.root.children[0] as ReactTestInstance;
    expect(outerLayer.type).toBe('div');
    const title = outerLayer.children[0] as ReactTestInstance;
    expect(title.type).toBe('h1');
    expect(title.children[0]).toBe('Yay! Welcome to umi!');
  });
});
