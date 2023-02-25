import React from 'react';
import styles from './index.css';
import Button from 'antd/es/button'
const BasicLayout: React.FC = props => {

  return (
    <div className={styles.normal}>
      <h1 className={styles.title}>
        <span>基金投资策略分析</span>
        <Button href="#/compare" target="_black"  className={styles["compare-btn"]} >策略比较</Button>
      </h1>
      {props.children}
    </div>
  );
};

export default BasicLayout;
