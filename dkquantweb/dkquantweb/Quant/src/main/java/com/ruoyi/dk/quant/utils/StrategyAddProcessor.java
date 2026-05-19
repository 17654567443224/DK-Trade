package com.ruoyi.dk.quant.utils;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.common.utils.SecurityUtils;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.dk.quant.domain.*;
import com.ruoyi.dk.quant.domain.BO.StrategyAddBO;
import com.ruoyi.dk.quant.service.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.Map;

/**
 * 策略添加处理器
 * 用于处理从前端传入的StrategyAddBO对象到保存策略的完整流程
 */
@Component
public class StrategyAddProcessor {
    private static final Logger log = LoggerFactory.getLogger(StrategyAddProcessor.class);

    @Resource
    private ISymbolSelectionTemplateService symbolSelectionTemplateService;

    @Resource
    private IOpenPositionTemplateService openPositionTemplateService;

    @Resource
    private IProfitLossTemplateService profitLossTemplateService;

    @Resource
    private IFundTemplateService fundTemplateService;

    @Resource
    private IStrategySymbolSelectionService symbolSelectionService;

    @Resource
    private IStrategyOpenPositionService openPositionService;

    @Resource
    private IStrategyProfitLossService profitLossService;

    @Resource
    private IStrategyFundService fundService;

    @Resource
    private IFunctionSymbolSelectionService functionSymbolSelectionService;

    @Resource
    private IFunctionOpenPositionService functionOpenPositionService;

    @Resource
    private IFunctionProfitLossService functionProfitLossService;

    @Resource
    private IFunctionFundService functionFundService;

    @Resource
    private IUserStrategyArgsService argsService;

    @Resource
    private IUserStrategyAccountService accountService;

    @Resource
    private IStrategyService strategyService;

    private final ObjectMapper objectMapper = new ObjectMapper();

    /**
     * 处理策略添加
     * 
     * @param strategyAddBO 前端传入的策略数据
     * @return 处理后的Strategy对象，可以直接保存
     */
    public Strategy processStrategyAdd(StrategyAddBO strategyAddBO) {
        if (strategyAddBO == null) {
            throw new RuntimeException("策略数据不能为空");
        }

        // 获取当前用户ID
        Long userId = SecurityUtils.getUserId();
        Long id = strategyAddBO.getId();
        Strategy strategy_ed = null;
        if (id != null){
        strategy_ed = strategyService.selectStrategyById(id);
        }
        String username = SecurityUtils.getUsername();

        log.info("开始处理用户[{}]的策略修改请求: {}", userId, strategyAddBO.getStrategyName());

        // 解析remark字段中的额外数据
        StrategyAddBO.StrategyExtraData extraData = parseExtraData(strategyAddBO.getRemark());
        if (extraData == null) {
            throw new RuntimeException("策略额外数据不能为空");
        }

        try {
            // 1. 处理选股策略
            Long symbolSelectionId = processSymbolSelection(extraData, userId);
            log.info("选股策略处理完成，ID: {}", symbolSelectionId);

            // 2. 处理开仓策略
            Long openPositionId = processOpenPosition(extraData, userId);
            log.info("开仓策略处理完成，ID: {}", openPositionId);

            // 3. 处理止盈止损策略
            Long profitLossId = processProfitLoss(extraData, userId);
            log.info("止盈止损策略处理完成，ID: {}", profitLossId);

            // 4. 处理资金管理策略
            Long fundId = processFund(extraData, userId);
            log.info("资金管理策略处理完成，ID: {}", fundId);
            // 5. 保存策略参数信息
            UserStrategyArgs userStrategyArgs;
            if (id == null){
                userStrategyArgs = new UserStrategyArgs();
                userStrategyArgs.setSymbolSelection(symbolSelectionId);
                userStrategyArgs.setOpenPosition(openPositionId);
                userStrategyArgs.setProfitLoss(profitLossId);
                userStrategyArgs.setFund(fundId);
                userStrategyArgs.setPv(-1L); // 默认不使用私有路径
                argsService.insertUserStrategyArgs(userStrategyArgs);
            }
            else {
                userStrategyArgs = argsService.selectUserStrategyArgsById(strategy_ed.getArgsId());
                userStrategyArgs.setSymbolSelection(symbolSelectionId);
                userStrategyArgs.setOpenPosition(openPositionId);
                userStrategyArgs.setProfitLoss(profitLossId);
                userStrategyArgs.setFund(fundId);
                argsService.updateUserStrategyArgs(userStrategyArgs);
            }
            log.info("策略参数保存完成，ID: {}", userStrategyArgs.getId());

            // 6. 创建策略账户
            UserStrategyAccount account = new UserStrategyAccount();
            account.setBalance(extraData.getCapital().toString());
            account.setOrderFee("0.0002");
            if (id != null) {
                Long accountId = strategy_ed.getAccountId();
                if (accountId != null){
                    accountService.updateUserStrategyAccount(account);
                }
            }
            else {
                accountService.insertUserStrategyAccount(account);
            }
            log.info("策略账户创建完成，ID: {}", account.getId());

            // 7. 创建策略对象
            Strategy strategy = new Strategy();
            if (id != null){
                strategy.setId(id);
            }
            strategy.setStrategyName(strategyAddBO.getStrategyName());
            strategy.setOwner(userId);
            strategy.setAccountId(account.getId());
            strategy.setLever(extraData.getLever());
            strategy.setMaxPosition(extraData.getMaxPositions().longValue());
            strategy.setArgsId(userStrategyArgs.getId());
            strategy.setRemark(username);
            strategy.setCreateBy(SecurityUtils.getUsername());
            strategy.setCreateTime(DateUtils.getNowDate());

            log.info("策略处理完成，准备保存: {}", strategy.getStrategyName());
            return strategy;
        } catch (Exception e) {
            log.error("处理策略添加失败", e);
            throw new RuntimeException("处理策略添加失败: " + e.getMessage(), e);
        }
    }

    /**
     * 解析额外数据
     */
    private StrategyAddBO.StrategyExtraData parseExtraData(String remark) {
        if (StringUtils.isEmpty(remark)) {
            return null;
        }

        try {
            return objectMapper.readValue(remark, StrategyAddBO.StrategyExtraData.class);
        } catch (JsonProcessingException e) {
            log.error("解析策略额外数据失败", e);
            throw new RuntimeException("解析策略额外数据失败: " + e.getMessage());
        }
    }

    /**
     * 处理选股策略
     */
    private Long processSymbolSelection(StrategyAddBO.StrategyExtraData extraData, Long userId) {
        // 1. 查询选股模板
        Long templateId = extraData.getStockSelectionTemplateId();
        if (templateId == null) {
            return null;
        }

        SymbolSelectionTemplate template = symbolSelectionTemplateService.selectSymbolSelectionTemplateById(templateId);
        if (template == null) {
            throw new RuntimeException("未找到选股策略模板: " + templateId);
        }

        // 2. 保存选股策略
        StrategySymbolSelection symbolSelection = new StrategySymbolSelection();
        symbolSelection.setOwner(userId);
        symbolSelection.setSymbolSelectionName(template.getCnClassName());
        symbolSelection.setFileName(template.getFileName());
        symbolSelection.setClassName(template.getClassName());

        // 设置策略参数 - 使用前端传入的参数
        Map<String, Object> args = extraData.getStockSelectionParams();
        if (args == null) {
            args = template.getClassArgs(); // 如果前端未传入参数，使用模板默认参数
        }
        symbolSelection.setArgs(args);

        // 保存选股策略
        symbolSelectionService.insertStrategySymbolSelection(symbolSelection);

        // 3. 保存选股方法,如果有方法的话

        if (!StringUtils.isEmpty(template.getFunName()) && !StringUtils.isEmpty(template.getCnFunName())) {
            FunctionSymbolSelection functionSymbolSelection = new FunctionSymbolSelection();
            functionSymbolSelection.setSymbolSelectionId(symbolSelection.getId());
            functionSymbolSelection.setFunName(template.getCnFunName());
            functionSymbolSelection.setFunc(template.getFunName());

            // 设置方法参数 - 使用前端传入的参数
            Map<String, Object> methodArgs = extraData.getStockSelectionMethodParams();
            if (methodArgs == null) {
                methodArgs = template.getFunArgs(); // 如果前端未传入参数，使用模板默认参数
            }
            functionSymbolSelection.setArgs(methodArgs);

            // 保存选股方法
            functionSymbolSelectionService.insertFunctionSymbolSelection(functionSymbolSelection);
        }
        return symbolSelection.getId();
    }

    /**
     * 处理开仓策略
     */
    private Long processOpenPosition(StrategyAddBO.StrategyExtraData extraData, Long userId) {
        // 1. 查询开仓模板
        Long templateId = extraData.getEntryTemplateId();
        if (templateId == null) {
            return null;
        }

        OpenPositionTemplate template = openPositionTemplateService.selectOpenPositionTemplateById(templateId);
        if (template == null) {
            throw new RuntimeException("未找到开仓策略模板: " + templateId);
        }

        // 2. 保存开仓策略
        StrategyOpenPosition openPosition = new StrategyOpenPosition();
        openPosition.setOwner(userId);
        openPosition.setOpenPositionName(template.getCnClassName());
        openPosition.setFileName(template.getFileName());
        openPosition.setClassName(template.getClassName());

        // 设置策略参数 - 使用前端传入的参数
        Map<String, Object> args = extraData.getEntryParams();
        if (args == null) {
            args = template.getClassArgs(); // 如果前端未传入参数，使用模板默认参数
        }

        // 如果有自定义公式，将公式数据添加到args中
        if (extraData.getCustomFormula() != null) {
            // 将自定义公式添加到args中
            if (args == null) {
                args = new HashMap<>();
            }
            args.put("strategy", extraData.getCustomFormula());
        }

        openPosition.setArgs(args);

        // 保存开仓策略
        openPositionService.insertStrategyOpenPosition(openPosition);

        // 3. 保存开仓方法
        if (!StringUtils.isEmpty(template.getFunName()) && !StringUtils.isEmpty(template.getCnFunName())) {
            FunctionOpenPosition functionOpenPosition = new FunctionOpenPosition();
            functionOpenPosition.setOpenPositionId(openPosition.getId());
            functionOpenPosition.setFunName(template.getFunName());
            functionOpenPosition.setFunc(template.getCnFunName());

            // 设置方法参数 - 使用前端传入的参数
            Map<String, Object> methodArgs = extraData.getEntryMethodParams();
            if (methodArgs == null) {
                methodArgs = template.getFunArgs(); // 如果前端未传入参数，使用模板默认参数
            }
            functionOpenPosition.setArgs(methodArgs);

            // 保存开仓方法
            functionOpenPositionService.insertFunctionOpenPosition(functionOpenPosition);
        }
        return openPosition.getId();
    }

    /**
     * 处理止盈止损策略
     */
    private Long processProfitLoss(StrategyAddBO.StrategyExtraData extraData, Long userId) {
        // 1. 查询止盈止损模板
        Long templateId = extraData.getStopLossTemplateId();
        if (templateId == null) {
            return null;
        }

        ProfitLossTemplate template = profitLossTemplateService.selectProfitLossTemplateById(templateId);
        if (template == null) {
            throw new RuntimeException("未找到止盈止损策略模板: " + templateId);
        }

        // 2. 保存止盈止损策略
        StrategyProfitLoss profitLoss = new StrategyProfitLoss();
        profitLoss.setOwner(userId);
        profitLoss.setProfitLossName(template.getCnClassName());
        profitLoss.setFileName(template.getFileName());
        profitLoss.setClassName(template.getClassName());

        // 设置策略参数 - 使用前端传入的参数
        Map<String, Object> args = extraData.getStopLossParams();
        if (args == null) {
            args = template.getClassArgs(); // 如果前端未传入参数，使用模板默认参数
        }
        profitLoss.setArgs(args);

        // 保存止盈止损策略
        profitLossService.insertStrategyProfitLoss(profitLoss);

        // 3. 保存止盈止损方法

        if (!StringUtils.isEmpty(template.getFunName()) && !StringUtils.isEmpty(template.getCnFunName())) {
            FunctionProfitLoss functionProfitLoss = new FunctionProfitLoss();
            functionProfitLoss.setProfitLossId(profitLoss.getId());
            functionProfitLoss.setFunName(template.getCnFunName());
            functionProfitLoss.setFunc(template.getFunName());

            // 设置方法参数 - 使用前端传入的参数
            Map<String, Object> methodArgs = extraData.getStopLossMethodParams();
            if (methodArgs == null) {
                methodArgs = template.getFunArgs(); // 如果前端未传入参数，使用模板默认参数
            }
            functionProfitLoss.setArgs(methodArgs);

            // 保存止盈止损方法
            functionProfitLossService.insertFunctionProfitLoss(functionProfitLoss);
        }
        return profitLoss.getId();
    }

    /**
     * 处理资金管理策略
     */
    private Long processFund(StrategyAddBO.StrategyExtraData extraData, Long userId) {
        // 1. 查询资金管理模板
        Long templateId = extraData.getPositionTemplateId();
        if (templateId == null) {
            return null;
        }

        FundTemplate template = fundTemplateService.selectFundTemplateById(templateId);
        if (template == null) {
            throw new RuntimeException("未找到资金管理策略模板: " + templateId);
        }

        // 2. 保存资金管理策略
        StrategyFund fund = new StrategyFund();
        fund.setOwner(userId);
        fund.setFundName(template.getCnClassName());
        fund.setFileName(template.getFileName());
        fund.setClassName(template.getClassName());

        // 设置策略参数 - 使用前端传入的参数
        Map<String, Object> args = extraData.getPositionParams();
        if (args == null) {
            args = template.getClassArgs(); // 如果前端未传入参数，使用模板默认参数
        }
        fund.setArgs(args);

        // 保存资金管理策略
        fundService.insertStrategyFund(fund);

        // 3. 保存资金管理方法
        if (!StringUtils.isEmpty(template.getFunName()) && !StringUtils.isEmpty(template.getCnFunName())) {
            FunctionFund functionFund = new FunctionFund();
            functionFund.setFundId(fund.getId());
            functionFund.setFunName(template.getCnFunName());
            functionFund.setFunc(template.getFunName());

            // 设置方法参数 - 使用前端传入的参数
            Map<String, Object> methodArgs = extraData.getPositionMethodParams();
            if (methodArgs == null) {
                methodArgs = template.getFunArgs(); // 如果前端未传入参数，使用模板默认参数
            }
            functionFund.setArgs(methodArgs);

            // 保存资金管理方法
            functionFundService.insertFunctionFund(functionFund);
        }
        return fund.getId();
    }
} 