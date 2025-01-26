import { Select } from 'antd';
import React from 'react';

interface SelectButtonProps {
  options: { value: string, label: string }[];
  onChange: (value: string | null) => void;
}

const SelectButton: React.FC<SelectButtonProps> = ({ options, onChange }) => {
  const sortedOptions = options.sort((a, b) => {
    const [monthA, yearA] = a.value.split('/');
    const [monthB, yearB] = b.value.split('/');
    const dateA = new Date(`${yearA}-${monthA}-01`);
    const dateB = new Date(`${yearB}-${monthB}-01`);
    return dateA.getTime() - dateB.getTime();
  });

  const extendedOptions = [{ value: '', label: 'Remover Filtro' }, ...sortedOptions];

  return (
    <Select
      className="select-button"
      showSearch
      style={{ width: 200 }}
      placeholder="Search to Select"
      optionFilterProp="label"
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