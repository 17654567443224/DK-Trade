package com.ruoyi.dk.quant.domain;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

import java.util.Map;

/**
 * 选股策略对象 strategy_symbol_selection
 * 
 * @author ruoyi
 * @date 2025-02-27
 */
@ApiModel(description = "选股策略")
public class StrategySymbolSelection extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** id */
    @ApiModelProperty("数据库id")
    private Long id;

    /** 归属 */
    @ApiModelProperty("归属（用户id）")
    @Excel(name = "归属")
    private Long owner;

    /** 选股策略名称 */
    @ApiModelProperty("选股策略名称")
    @Excel(name = "选股策略名称")
    private String symbolSelectionName;

    /** 文件名 */
    @ApiModelProperty("文件名")
    @Excel(name = "文件名")
    private String fileName;

    /** 类名 */
    @ApiModelProperty("类名")
    @Excel(name = "类名")
    private String className;

    /** 参数 */
    @ApiModelProperty("参数")
    @Excel(name = "参数")
    private Map<String, Object> args;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setOwner(Long owner) 
    {
        this.owner = owner;
    }

    public Long getOwner() 
    {
        return owner;
    }
    public void setSymbolSelectionName(String symbolSelectionName) 
    {
        this.symbolSelectionName = symbolSelectionName;
    }

    public String getSymbolSelectionName() 
    {
        return symbolSelectionName;
    }
    public void setFileName(String fileName) 
    {
        this.fileName = fileName;
    }

    public String getFileName() 
    {
        return fileName;
    }
    public void setClassName(String className) 
    {
        this.className = className;
    }

    public String getClassName() 
    {
        return className;
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
            .append("owner", getOwner())
            .append("symbolSelectionName", getSymbolSelectionName())
            .append("fileName", getFileName())
            .append("className", getClassName())
            .append("args", getArgs())
            .toString();
    }
}
