from sku_mapper import SKUMappingEngine
import pandas as pd

engine = SKUMappingEngine(
    sku_to_msku_path=r"C:\Users\Charan singh\Desktop\wms_mvp_project\WMS-04-02 - Msku With Skus.csv",
    combo_path=r"C:\Users\Charan singh\Desktop\wms_mvp_project\WMS-04-02 - Combos skus.csv"
)

sales_df = pd.read_csv("Cste FK.csv")
mapped_df = engine.map_sales_data(sales_df)
mapped_df.to_csv("mapped_output.csv", index=False)
print(mapped_df.head())
