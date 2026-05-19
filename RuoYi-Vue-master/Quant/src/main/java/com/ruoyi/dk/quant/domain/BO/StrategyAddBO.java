package com.ruoyi.dk.quant.domain.BO;

import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import java.util.List;
import java.util.Map;

@ApiModel(description = "创建或更新策略请求")
public class StrategyAddBO {

    @ApiModelProperty("策略ID，更新时提供")
    private Long id;

    @ApiModelProperty("策略名称")
    private String strategyName;

    @ApiModelProperty(value = "策略备注和额外数据的JSON字符串", notes = "包含额外的策略配置信息")
    private String remark;

    @ApiModelProperty("策略组件参数")
    private StrategyParameters parameters;

    @ApiModel(description = "策略组件参数")
    public static class StrategyParameters {

        @ApiModelProperty("选股策略ID")
        private Long stockSelection;

        @ApiModelProperty("开仓策略ID")
        private Long entry;

        @ApiModelProperty("止盈止损策略ID")
        private Long stopLoss;

        @ApiModelProperty("资金管理策略ID")
        private Long position;

        // Getters and Setters
        public Long getStockSelection() {
            return stockSelection;
        }

        public void setStockSelection(Long stockSelection) {
            this.stockSelection = stockSelection;
        }

        public Long getEntry() {
            return entry;
        }

        public void setEntry(Long entry) {
            this.entry = entry;
        }

        public Long getStopLoss() {
            return stopLoss;
        }

        public void setStopLoss(Long stopLoss) {
            this.stopLoss = stopLoss;
        }

        public Long getPosition() {
            return position;
        }

        public void setPosition(Long position) {
            this.position = position;
        }
    }

    @ApiModel(description = "策略额外数据")
    public static class StrategyExtraData {

        @ApiModelProperty("本金")
        private Long capital;

        @ApiModelProperty("最大持仓数量")
        private Integer maxPositions;

        @ApiModelProperty("杠杆倍数")
        private String lever;

        @ApiModelProperty("选股模板ID")
        private Long stockSelectionTemplateId;

        @ApiModelProperty("选股方法")
        private String stockSelectionMethod;

        @ApiModelProperty("选股参数")
        private Map<String, Object> stockSelectionParams;

        @ApiModelProperty("选股方法参数")
        private Map<String, Object> stockSelectionMethodParams;

        @ApiModelProperty("开仓模板ID")
        private Long entryTemplateId;

        @ApiModelProperty("开仓方法")
        private String entryMethod;

        @ApiModelProperty("开仓参数")
        private Map<String, Object> entryParams;

        @ApiModelProperty("开仓方法参数")
        private Map<String, Object> entryMethodParams;

        @ApiModelProperty("止盈止损模板ID")
        private Long stopLossTemplateId;

        @ApiModelProperty("止盈止损方法")
        private String stopLossMethod;

        @ApiModelProperty("止盈止损参数")
        private Map<String, Object> stopLossParams;

        @ApiModelProperty("止盈止损方法参数")
        private Map<String, Object> stopLossMethodParams;

        @ApiModelProperty("资金管理模板ID")
        private Long positionTemplateId;

        @ApiModelProperty("资金管理方法")
        private String positionMethod;

        @ApiModelProperty("资金管理参数")
        private Map<String, Object> positionParams;

        @ApiModelProperty("资金管理方法参数")
        private Map<String, Object> positionMethodParams;

        @ApiModelProperty("自定义公式数据")
        private CustomFormulaData customFormula;

        // Getters and Setters
        public Long getCapital() {
            return capital;
        }

        public void setCapital(Long capital) {
            this.capital = capital;
        }

        public Integer getMaxPositions() {
            return maxPositions;
        }

        public void setMaxPositions(Integer maxPositions) {
            this.maxPositions = maxPositions;
        }

        public String getLever() {return lever;}

        public void setLever(String lever) {this.lever = lever;}

        public Long getStockSelectionTemplateId() {
            return stockSelectionTemplateId;
        }

        public void setStockSelectionTemplateId(Long stockSelectionTemplateId) {
            this.stockSelectionTemplateId = stockSelectionTemplateId;
        }

        public String getStockSelectionMethod() {
            return stockSelectionMethod;
        }

        public void setStockSelectionMethod(String stockSelectionMethod) {
            this.stockSelectionMethod = stockSelectionMethod;
        }

        public Map<String, Object> getStockSelectionParams() {
            return stockSelectionParams;
        }

        public void setStockSelectionParams(Map<String, Object> stockSelectionParams) {
            this.stockSelectionParams = stockSelectionParams;
        }

        public Map<String, Object> getStockSelectionMethodParams(){
            return stockSelectionMethodParams;
        }

        public void setStockSelectionMethodParams(Map<String, Object> stockSelectionMethodParams){
            this.stockSelectionMethodParams = stockSelectionMethodParams;
        }

        public Long getEntryTemplateId() {
            return entryTemplateId;
        }

        public void setEntryTemplateId(Long entryTemplateId) {
            this.entryTemplateId = entryTemplateId;
        }

        public String getEntryMethod() {
            return entryMethod;
        }

        public void setEntryMethod(String entryMethod) {
            this.entryMethod = entryMethod;
        }

        public Map<String, Object> getEntryParams() {
            return entryParams;
        }

        public void setEntryParams(Map<String, Object> entryParams) {
            this.entryParams = entryParams;
        }

        public Map<String, Object> getEntryMethodParams() {
            return entryMethodParams;
        }

        public void setEntryMethodParams(Map<String, Object> entryMethodParams) {
            this.entryMethodParams = entryMethodParams;
        }

        public Long getStopLossTemplateId() {
            return stopLossTemplateId;
        }

        public void setStopLossTemplateId(Long stopLossTemplateId) {
            this.stopLossTemplateId = stopLossTemplateId;
        }

        public String getStopLossMethod() {
            return stopLossMethod;
        }

        public void setStopLossMethod(String stopLossMethod) {
            this.stopLossMethod = stopLossMethod;
        }

        public Map<String, Object> getStopLossParams() {
            return stopLossParams;
        }

        public void setStopLossParams(Map<String, Object> stopLossParams) {
            this.stopLossParams = stopLossParams;
        }

        public Map<String, Object> getStopLossMethodParams() {
            return stopLossMethodParams;
        }

        public void setStopLossMethodParams(Map<String, Object> stopLossMethodParams) {
            this.stopLossMethodParams = stopLossMethodParams;
        }

        public Long getPositionTemplateId() {
            return positionTemplateId;
        }

        public void setPositionTemplateId(Long positionTemplateId) {
            this.positionTemplateId = positionTemplateId;
        }

        public String getPositionMethod() {
            return positionMethod;
        }

        public void setPositionMethod(String positionMethod) {
            this.positionMethod = positionMethod;
        }

        public Map<String, Object> getPositionParams() {
            return positionParams;
        }

        public void setPositionParams(Map<String, Object> positionParams) {
            this.positionParams = positionParams;
        }

        public Map<String, Object> getPositionMethodParams() {
            return positionMethodParams;
        }

        public void setPositionMethodParams(Map<String, Object> positionMethodParams) {
            this.positionMethodParams = positionMethodParams;
        }

        public CustomFormulaData getCustomFormula() {
            return customFormula;
        }

        public void setCustomFormula(CustomFormulaData customFormula) {
            this.customFormula = customFormula;
        }
    }

    @ApiModel(description = "自定义公式数据")
    public static class CustomFormulaData {

        @ApiModelProperty("公式标签(指标)")
        private List<String> label;

        @ApiModelProperty("公式操作")
        private List<String> action;

        @ApiModelProperty("K线数据")
        private List<String> bar;

        @ApiModelProperty("参数列表")
        private List<Map<String, Map<String, Object>>> args;

        // Getters and Setters
        public List<String> getLabel() {
            return label;
        }

        public void setLabel(List<String> label) {
            this.label = label;
        }

        public List<String> getAction() {
            return action;
        }

        public void setAction(List<String> action) {
            this.action = action;
        }

        public List<String> getBar() {
            return bar;
        }

        public void setBar(List<String> bar) {
            this.bar = bar;
        }

        public List<Map<String, Map<String, Object>>> getArgs() {
            return args;
        }

        public void setArgs(List<Map<String, Map<String, Object>>> args) {
            this.args = args;
        }
    }
    @ApiModel(description = "公式参数")
    public static class FormulaArg {

        @ApiModelProperty("参数名称")
        private String name;

        @ApiModelProperty("参数值")
        private Object value;

        @ApiModelProperty("参数描述")
        private String description;

        // Getters and Setters
        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public Object getValue() {
            return value;
        }

        public void setValue(Object value) {
            this.value = value;
        }

        public String getDescription() {
            return description;
        }

        public void setDescription(String description) {
            this.description = description;
        }
    }

    // Getters and Setters for StrategyRequestDTO
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getStrategyName() {
        return strategyName;
    }

    public void setStrategyName(String strategyName) {
        this.strategyName = strategyName;
    }


    public String getRemark() {
        return remark;
    }

    public void setRemark(String remark) {
        this.remark = remark;
    }

    public StrategyParameters getParameters() {
        return parameters;
    }

    public void setParameters(StrategyParameters parameters) {
        this.parameters = parameters;
    }
}