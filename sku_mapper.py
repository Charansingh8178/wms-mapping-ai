import pandas as pd

class SKUMappingEngine:
    def __init__(self, sku_to_msku_path, combo_path):
        self.sku_df = pd.read_csv(sku_to_msku_path)
        self.combo_df = pd.read_csv(combo_path)
        self.mapping_dict = {}
        self.combo_dict = {}
        self.build_mappings()

    def build_mappings(self):
        self.sku_df.columns = self.sku_df.columns.str.lower()
        self.combo_df.columns = self.combo_df.columns.str.lower()

        for _, row in self.sku_df.iterrows():
            sku = str(row.get('sku', '')).strip()
            msku = str(row.get('msku', '')).strip()
            if sku and msku:
                self.mapping_dict[sku] = msku
                self.mapping_dict[msku] = msku  # allow direct MSKU match too

        for _, row in self.combo_df.iterrows():
            combo = str(row.get('combo', '')).strip()
            self.combo_dict[combo] = {}
            for key, val in row.items():
                if key.startswith('sku') and pd.notnull(val):
                    part_sku = str(val).strip()
                    part_msku = self.mapping_dict.get(part_sku)
                    if part_msku:
                        self.combo_dict[combo][part_msku] = self.combo_dict[combo].get(part_msku, 0) + 1

    def map_sales_data(self, sales_df):
        result_rows = []
        sales_df.columns = sales_df.columns.str.lower().str.strip()

        sku_col = (
            'sku' if 'sku' in sales_df.columns else
            'fnsku' if 'fnsku' in sales_df.columns else
            'msku' if 'msku' in sales_df.columns else None
        )
        if not sku_col:
            raise ValueError("SKU/MSKU/FNSKU column not found in sales data.")

        for _, row in sales_df.iterrows():
            sku = str(row.get(sku_col, '')).strip()
            qty = int(row.get('quantity', 1)) if pd.notnull(row.get('quantity')) else 1

            order_id = (
                row.get('orderid') or
                row.get('order id') or
                row.get('reference id') or
                row.get('reference_id') or
                row.get('order-number') or
                row.get('sub order no') or
                row.get('order number') or ''
            )
            order_id = str(order_id).strip()

            if sku in self.mapping_dict:
                result_rows.append({
                    'OrderID': order_id,
                    'SKU': sku,
                    'MSKU': self.mapping_dict[sku],
                    'Mapped_Qty': qty,
                    'Status': 'Mapped'
                })
            elif sku in self.combo_dict:
                for msku, mult_qty in self.combo_dict[sku].items():
                    result_rows.append({
                        'OrderID': order_id,
                        'SKU': sku,
                        'MSKU': msku,
                        'Mapped_Qty': qty * mult_qty,
                        'Status': 'Combo Mapped'
                    })
            else:
                result_rows.append({
                    'OrderID': order_id,
                    'SKU': sku,
                    'MSKU': '',
                    'Mapped_Qty': qty,
                    'Status': 'Unmapped'
                })

        return pd.DataFrame(result_rows)
