package com.ruoyi.dk.quant.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 策略订单信息对象 user_strategy_orders
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@ApiModel(description = "策略订单信息")
public class UserStrategyOrders extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** id */
    @ApiModelProperty("数据库id")
    private Long id;

    /** 策略id */
    @ApiModelProperty("策略id")
    @Excel(name = "策略id")
    private Long strategyId;

    /** 交易对 */
    @ApiModelProperty("交易对")
    @Excel(name = "交易对")
    private String symbol;

    /** 交易对 */
    @ApiModelProperty("杠杆倍数")
    @Excel(name = "杠杆倍数")
    private String lever;

    /** 开平类型 */
    @ApiModelProperty("开平类型")
    @Excel(name = "开平类型")
    private String type;

    /** 开仓均价 */
    @ApiModelProperty("开仓均价")
    @Excel(name = "开仓均价")
    private String entryPrice;

    /** 平仓均价 */
    @ApiModelProperty("平仓均价")
    @Excel(name = "平仓均价")
    private String price;

    /** 数量 */
    @ApiModelProperty("数量")
    @Excel(name = "数量")
    private String sz;

    /** 平仓时间 */
    @ApiModelProperty("平仓时间")
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "平仓时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date time;

    /** 收益 */
    @ApiModelProperty("收益")
    @Excel(name = "收益")
    private String pnl;

    /** 收益率 */
    @ApiModelProperty("收益率")
    @Excel(name = "收益率")
    private String pnlRatio;

    /** 平仓类型 */
    @ApiModelProperty("平仓类型")
    @Excel(name = "平仓类型")
    private String exitType;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setStrategyId(Long strategyId) 
    {
        this.strategyId = strategyId;
    }

    public Long getStrategyId() 
    {
        return strategyId;
    }
    public void setSymbol(String symbol) 
    {
        this.symbol = symbol;
    }

    public String getSymbol() 
    {
        return symbol;
    }

    public void setLever(String lever) {this.lever = lever;}

    public String getLever(){return lever;}

    public void setType(String type) 
    {
        this.type = type;
    }

    public String getType() 
    {
        return type;
    }
    public void setEntryPrice(String entryPrice) 
    {
        this.entryPrice = entryPrice;
    }

    public String getEntryPrice() 
    {
        return entryPrice;
    }
    public void setPrice(String price) 
    {
        this.price = price;
    }

    public String getPrice() 
    {
        return price;
    }
    public void setSz(String sz) 
    {
        this.sz = sz;
    }

    public String getSz() 
    {
        return sz;
    }
    public void setTime(Date time) 
    {
        this.time = time;
    }

    public Date getTime() 
    {
        return time;
    }
    public void setPnl(String pnl) 
    {
        this.pnl = pnl;
    }

    public String getPnl() 
    {
        return pnl;
    }
    public void setPnlRatio(String pnlRatio) 
    {
        this.pnlRatio = pnlRatio;
    }

    public String getPnlRatio() 
    {
        return pnlRatio;
    }
    public void setExitType(String exitType) 
    {
        this.exitType = exitType;
    }

    public String getExitType() 
    {
        return exitType;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("strategyId", getStrategyId())
            .append("symbol", getSymbol())
            .append("type", getType())
            .append("entryPrice", getEntryPrice())
            .append("price", getPrice())
            .append("sz", getSz())
            .append("time", getTime())
            .append("pnl", getPnl())
            .append("pnlRatio", getPnlRatio())
            .append("exitType", getExitType())
            .toString();
    }
}
