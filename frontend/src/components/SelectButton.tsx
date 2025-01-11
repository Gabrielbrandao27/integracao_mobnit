import { Select } from 'antd';
import React from 'react';

interface SelectButtonProps {
  options: { value: string, label: string }[];
  onChange: (value: string) => void;
}

const SelectButton: React.FC<SelectButtonProps> = ({ options, onChange }) => (
  <Select
    className='select-button'
    showSearch
    style={{ width: 200 }}
    placeholder="Search to Select"
    optionFilterProp="label"
    filterSort={(optionA, optionB) =>
      (optionA?.label ?? '').toLowerCase().localeCompare((optionB?.label ?? '').toLowerCase())
    }
    options={options}
    onChange={onChange}
  />
);

export default SelectButton;