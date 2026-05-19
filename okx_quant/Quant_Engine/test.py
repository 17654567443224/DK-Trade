from Quant_Engine.template.profit_loss_template.base_template import Base_Template
a = Base_Template(lever=100, sl_percent=50, tp_percent=50)
print(a.get_percentage_levels("a", td=1, avg_price=1500))