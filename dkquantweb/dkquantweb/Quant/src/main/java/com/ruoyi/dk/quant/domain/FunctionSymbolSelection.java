package com.ruoyi.dk.quant.domain;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

import java.util.Map;

/**
 * 选股方法对象 func_symbol_selection
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@ApiModel(description = "选股方法")
public class FunctionSymbolSelection extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** id */
    @ApiModelProperty("数据库id")
    private Long id;

    /** 上级id */
    @Excel(name = "上级id")
    @ApiModelProperty("上级id")
    private Long symbolSelectionId;

    /** 方法名称 */
    @ApiModelProperty("方法名称")
    @Excel(name = "方法名称")
    private String funName;

    /** 方法 */
    @ApiModelProperty("方法")
    @Excel(name = "方法")
    private String func;

    /** 方法参数 */
    @ApiModelProperty("方法参数")
    @Excel(name = "方法参数")
    private Map<String, Object> args;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setSymbolSelectionId(Long symbolSelectionId) 
    {
        this.symbolSelectionId = symbolSelectionId;
    }

    public Long getSymbolSelectionId() 
    {
        return symbolSelectionId;
    }
    public void setFunName(String funName) 
    {
        this.funName = funName;
    }

    public String getFunName() 
    {
        return funName;
    }
    public void setFunc(String func) 
    {
        this.func = func;
    }

    public String getFunc() 
    {
        return func;
    }
    public void setArgs(Map<String, Object> args)
    {
        this.args = args;
    }

    public Map<String, Object> getArgs()
    {
        return args;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("symbolSelectionId", getSymbolSelectionId())
            .append("funName", getFunName())
            .append("func", getFunc())
            .append("args", getArgs())
            .toString();
    }
}
