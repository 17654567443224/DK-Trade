package com.ruoyi.dk.quant.domain;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 策略对象 strategy
 * 
 * @author ruoyi
 * @date 2025-02-16
 */
@ApiModel(description = "策略")
public class Strategy extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 策略id */
    @ApiModelProperty("策略id")
    private Long id;

    /** 策略名称 */
    @ApiModelProperty("策略名称")
    @Excel(name = "策略名称")
    private String strategyName;

    /** 归属(用户id) */
    @ApiModelProperty("归属(用户id)")
    @Excel(name = "归属")
    private Long owner;

    /** 本金 */
    @ApiModelProperty("本金")
    @Excel(name = "本金")
    private Long accountId;

    @ApiModelProperty("杠杆")
    @Excel(name = "杠杆")
    private String lever;

    /** 最多持仓 */
    @ApiModelProperty("最多持仓")
    @Excel(name = "最多持仓")
    private Long maxPosition;

    /** 参数 */
    @ApiModelProperty("参数")
    @Excel(name = "参数")
    private Long argsId;

    /** 删除标志（0代表存在 2代表删除） */
    private String delFlag;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setStrategyName(String strategyName) 
    {
        this.strategyName = strategyName;
    }

    public String getStrategyName() 
    {
        return strategyName;
    }
    public void setOwner(Long owner)
    {
        this.owner = owner;
    }

    public Long getOwner()
    {
        return owner;
    }
    public void setAccountId(Long accountId)
    {
        this.accountId = accountId;
    }

    public Long getAccountId()
    {
        return accountId;
    }

    public String getLever(){return lever;}

    public void setLever(String lever){this.lever = lever;}

    public void setMaxPosition(Long maxPosition) 
    {
        this.maxPosition = maxPosition;
    }

    public Long getMaxPosition() 
    {
        return maxPosition;
    }
    public void setArgsId(Long argsId)
    {
        this.argsId = argsId;
    }

    public Long getArgsId()
    {
        return argsId;
    }
    public void setDelFlag(String delFlag) 
    {
        this.delFlag = delFlag;
    }

    public String getDelFlag() 
    {
        return delFlag;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("strategyName", getStrategyName())
            .append("owner", getOwner())
            .append("accountId", getAccountId())
            .append("maxPosition", getMaxPosition())
            .append("args", getArgsId())
            .append("delFlag", getDelFlag())
            .append("createBy", getCreateBy())
            .append("createTime", getCreateTime())
            .append("updateBy", getUpdateBy())
            .append("updateTime", getUpdateTime())
            .append("remark", getRemark())
            .toString();
    }
}
