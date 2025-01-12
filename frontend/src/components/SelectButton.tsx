import { Select } from 'antd';
import React from 'react';

interface SelectButtonProps {
  options: { value: string, label: string }[];
  onChange: (value: string | null) => void;
}

const SelectButton: React.FC<SelectButtonProps> = ({ options, onChange }) => {
  const extendedOptions = [{ value: '', label: 'Remover Filtro' }, ...options];

  return (
    <Select
      className="select-button"
      showSearch
      style={{ width: 200 }}
      placeholder="Search to Select"
      optionFilterProp="label"
      filterSort={(optionA, optionB) =>
        (optionA?.label ?? '').toLowerCase().localeCompare((optionB?.label ?? '').toLowerCase())
      }
      options={extendedOptions}
      onChange={(value) => {
        if (value === '') {
          onChange(null);
        } else {
          onChange(value);
        }
      }}
    />
  );
};

export default SelectButton;
