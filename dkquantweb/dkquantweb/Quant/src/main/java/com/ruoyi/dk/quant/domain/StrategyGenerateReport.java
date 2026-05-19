package com.ruoyi.dk.quant.domain;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 策略绩效指标对象 strategy_generate_report
 * 
 * @author ruoyi
 * @date 2025-02-15
 */
@ApiModel(description = "策略绩效指标")
public class StrategyGenerateReport
{
    private static final long serialVersionUID = 1L;

    /** 策略ID */
    @ApiModelProperty("数据库id")
    private Long id;

    /** 策略ID */
    @ApiModelProperty("策略id")
    @Excel(name = "策略id")
    private Long strategyId;

    /** 余额 */
    @ApiModelProperty("余额")
    @Excel(name = "余额")
    private Long finalBalance;

    /** 最大回撤 */
    @ApiModelProperty("最大回撤")
    @Excel(name = "最大回撤")
    private Long maxDrawdown;

    /** 胜率 */
    @ApiModelProperty("胜率")
    @Excel(name = "胜率")
    private Long winRate;

    /** 最大盈利 */
    @ApiModelProperty("最大盈利")
    @Excel(name = "最大盈利")
    private Long maxProfit;

    /** 最大亏损 */
    @ApiModelProperty("最大亏损")
    @Excel(name = "最大亏损")
    private Long maxLoss;

    /** 交易总数 */
    @ApiModelProperty("交易总数")
    @Excel(name = "交易总数")
    private Long totalTrades;

    /** 夏普比率 */
    @ApiModelProperty("夏普比率")
    @Excel(name = "夏普比率")
    private Long sharpeRatio;

    /** 年化 */
    @ApiModelProperty("年化")
    @Excel(name = "年化")
    private Long annualizedReturn;

    /** 总收益率 */
    @ApiModelProperty("总收益率")
    @Excel(name = "总收益率")
    private Long totalPnlratio;

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
    public void setFinalBalance(Long finalBalance) 
    {
        this.finalBalance = finalBalance;
    }

    public Long getFinalBalance() 
    {
        return finalBalance;
    }
    public void setMaxDrawdown(Long maxDrawdown) 
    {
        this.maxDrawdown = maxDrawdown;
    }

    public Long getMaxDrawdown() 
    {
        return maxDrawdown;
    }
    public void setWinRate(Long winRate) 
    {
        this.winRate = winRate;
    }

    public Long getWinRate() 
    {
        return winRate;
    }
    public void setMaxProfit(Long maxProfit) 
    {
        this.maxProfit = maxProfit;
    }

    public Long getMaxProfit() 
    {
        return maxProfit;
    }
    public void setMaxLoss(Long maxLoss) 
    {
        this.maxLoss = maxLoss;
    }

    public Long getMaxLoss() 
    {
        return maxLoss;
    }
    public void setTotalTrades(Long totalTrades) 
    {
        this.totalTrades = totalTrades;
    }

    public Long getTotalTrades() 
    {
        return totalTrades;
    }
    public void setSharpeRatio(Long sharpeRatio) 
    {
        this.sharpeRatio = sharpeRatio;
    }

    public Long getSharpeRatio() 
    {
        return sharpeRatio;
    }
    public void setAnnualizedReturn(Long annualizedReturn) 
    {
        this.annualizedReturn = annualizedReturn;
    }

    public Long getAnnualizedReturn() 
    {
        return annualizedReturn;
    }
    public void setTotalPnlratio(Long totalPnlratio) 
    {
        this.totalPnlratio = totalPnlratio;
    }

    public Long getTotalPnlratio() 
    {
        return totalPnlratio;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
                .append("strategyId", getStrategyId())
            .append("finalBalance", getFinalBalance())
            .append("maxDrawdown", getMaxDrawdown())
            .append("winRate", getWinRate())
            .append("maxProfit", getMaxProfit())
            .append("maxLoss", getMaxLoss())
            .append("totalTrades", getTotalTrades())
            .append("sharpeRatio", getSharpeRatio())
            .append("annualizedReturn", getAnnualizedReturn())
            .append("totalPnlratio", getTotalPnlratio())
            .toString();
    }
}
