package com.ruoyi.dk.quant.service.impl;

import java.util.HashMap;
import java.util.List;

import com.alibaba.fastjson2.util.BeanUtils;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.domain.entity.SysUser;
import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.common.utils.SecurityUtils;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.dk.quant.client.PO.AddStrategy;
import com.ruoyi.dk.quant.client.PO.BaseStrategy;
import com.ruoyi.dk.quant.client.PRO.BaseResponse;
import com.ruoyi.dk.quant.client.PythonClient;
import com.ruoyi.dk.quant.domain.*;
import com.ruoyi.dk.quant.domain.BO.BackTestingBO;
import com.ruoyi.dk.quant.domain.BO.StrategyAddBO;
import com.ruoyi.dk.quant.domain.BO.StrategyBO;
import com.ruoyi.dk.quant.service.*;
import com.ruoyi.system.service.ISysUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.StrategyMapper;
import com.ruoyi.dk.quant.utils.StrategyAddProcessor;

import static com.ruoyi.dk.quant.client.FunctionConstants.*;


/**
 * 策略Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-02-16
 */
@Service
public class StrategyServiceImpl implements IStrategyService 
{
    @Autowired
    private StrategyMapper strategyMapper;

    @Autowired
    private PythonClient pythonClient;

    @Autowired
    private IUserStrategyAccountService accountService;

    @Autowired
    private IUserStrategyPositionService positionService;

    @Autowired
    private IUserStrategyOrdersService ordersService;

    @Autowired
    private IUserStrategyArgsService argsService;

    @Autowired
    private ISysUserService userService;

    @Autowired
    private IStrategyPvService pvService;

    @Autowired
    private IStrategySymbolSelectionService symbolSelectionService;

    @Autowired
    private IStrategyOpenPositionService openPositionService;

    @Autowired
    private IStrategyProfitLossService profitLossService;

    @Autowired
    private IStrategyFundService fundService;

    @Autowired
    private IFunctionSymbolSelectionService functionSymbolSelectionService;

    @Autowired
    private IFunctionOpenPositionService functionOpenPositionService;

    @Autowired
    private IFunctionProfitLossService functionProfitLossService;

    @Autowired
    private IFunctionFundService functionFundService;

    @Autowired
    private StrategyAddProcessor strategyAddProcessor;

    /**
     * 查询策略
     * 
     * @param id 策略主键
     * @return 策略
     */
    @Override
    public Strategy selectStrategyById(Long id)
    {

        return strategyMapper.selectStrategyById(id);
    }

    /**
     * 查询策略列表
     * 
     * @param strategy 策略
     * @return 策略
     */
    @Override
    public List<Strategy> selectStrategyList(Strategy strategy)
    {
        Long userId = SecurityUtils.getUserId();
        if (StringUtils.isNotNull(userId)){  //查询公共策略
            strategy.setOwner(1L);
            return strategyMapper.selectStrategyList(strategy);
        }
        strategy.setOwner(userId);
        return strategyMapper.selectStrategyList(strategy);
    }

    /**
     * 新增策略 - 处理前端传入的StrategyAddBO对象
     * 
     * @param strategyAddBO 前端提交的策略数据
     * @return 结果
     */
    @Override
    public Long insertStrategy(StrategyAddBO strategyAddBO) {
        try {
            // 使用策略添加处理器处理数据
            Strategy strategy = strategyAddProcessor.processStrategyAdd(strategyAddBO);
            
            // 保存策略并返回结果
            strategyMapper.insertStrategy(strategy);
            
            // 将生成的ID设置回传入的对象
            strategyAddBO.setId(strategy.getId());
            
            return strategy.getId();
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("保存策略失败: " + e.getMessage());
        }
    }

    /**
     * 修改策略
     * 
     * @param strategyAddBO 策略
     * @return 结果
     */
    @Override
    public Long updateStrategy(StrategyAddBO strategyAddBO)
    {
        try {
            // 使用策略添加处理器处理数据
            Strategy strategy = strategyAddProcessor.processStrategyAdd(strategyAddBO);

            // 保存策略并返回结果
            strategyMapper.updateStrategy(strategy);

            // 将生成的ID设置回传入的对象
            strategyAddBO.setId(strategy.getId());

            return strategy.getId();
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException("修改策略失败: " + e.getMessage());
        }
    }

    /**
     * 批量删除策略
     * 
     * @param ids 需要删除的策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategyByIds(Long[] ids)
    {
        return strategyMapper.deleteStrategyByIds(ids);
    }

    /**
     * 删除策略信息
     * 
     * @param id 策略主键
     * @return 结果
     */
    @Override
    public int deleteStrategyById(Long id)
    {
        return strategyMapper.deleteStrategyById(id);
    }

    /**
     * 运行策略
     * @param strategyBO
     * @return
     */
    @Override
    public String addStrategy(StrategyBO strategyBO) throws JsonProcessingException {
        // 到数据库查找是否有该策略
        Long id = strategyBO.getId();
        Long owner = SecurityUtils.getUserId(); // 当前用户id
        Strategy strategy = strategyMapper.selectStrategyById(id);
        if (strategy == null){
            return "没有找到该策略，请重新添加";
        }
        Long strategyOwner = strategy.getOwner();
        if (strategyOwner.equals(owner) == Boolean.FALSE) { // 没有该策略
            SysUser sysUser = new SysUser();
            sysUser.setStatus("1");
            userService.updateUserStatus(sysUser);
            return "非法操作，账户已封禁";
        }
        //有该策略
        // 查询account信息
        Long accountId = strategy.getAccountId();
        UserStrategyAccount userStrategyAccount = accountService.selectUserStrategyAccountById(accountId);
        // 创建 ObjectMapper
        ObjectMapper objectMapper = new ObjectMapper();
        // 转换对象为 JSON 字符串
        String accountJson = objectMapper.writeValueAsString(userStrategyAccount);
        // 获取订单和仓位数据
        UserStrategyPosition userStrategyPosition = new UserStrategyPosition();
        userStrategyPosition.setStrategyId(id);
        List<UserStrategyPosition> positions = positionService.selectUserStrategyPositionList(userStrategyPosition);
        UserStrategyOrders userStrategyOrders = new UserStrategyOrders();
        userStrategyOrders.setStrategyId(id);
        List<UserStrategyOrders> orders = ordersService.selectUserStrategyOrdersList(userStrategyOrders);
        // 查询args信息
        Long argsId = strategy.getArgsId();
        UserStrategyArgs userStrategyArgs = argsService.selectUserStrategyArgsById(argsId);
        Long pv = userStrategyArgs.getPv();
        Long symbolSelection = userStrategyArgs.getSymbolSelection();
        Long openPosition = userStrategyArgs.getOpenPosition();
        Long profitLoss = userStrategyArgs.getProfitLoss();
        Long fund = userStrategyArgs.getFund();
        // 提取策略类信息
        AddStrategy strategyBuild = new AddStrategy();

        StrategySymbolSelection strategySymbolSelection = symbolSelectionService.selectStrategySymbolSelectionById(symbolSelection);
        StrategyOpenPosition strategyOpenPosition = openPositionService.selectStrategyOpenPositionById(openPosition);
        StrategyProfitLoss strategyProfitLoss = profitLossService.selectStrategyProfitLossById(profitLoss);
        StrategyFund strategyFund = fundService.selectStrategyFundById(fund);
        HashMap<String, Object> map = new HashMap<>();
        map.put("symbol_selection", strategySymbolSelection);
        map.put("open_position", strategyOpenPosition);
        map.put("profit_loss", strategyProfitLoss);
        map.put("fund", strategyFund);
        if (pv != -1){
            StrategyPv strategyPv = pvService.selectStrategyPvById(pv);
            map.put("pv", strategyPv);

        }
        HashMap<String, Object> funMap = new HashMap<>();
        String argsJson = objectMapper.writeValueAsString(map);
        // 提取策略方法信息
        Long symbolSelectionId = strategySymbolSelection.getId();
        Long openPositionId = null;
        if (strategyOpenPosition != null){
        openPositionId = strategyOpenPosition.getId();
        }
        Long profitLossId = strategyProfitLoss.getId();
        Long fundId = strategyFund.getId();

        FunctionSymbolSelection functionSymbolSelection = new FunctionSymbolSelection();
        functionSymbolSelection.setSymbolSelectionId(symbolSelectionId);
        List<FunctionSymbolSelection> ss_selections = functionSymbolSelectionService.selectFunctionSymbolSelectionList(functionSymbolSelection);
        FunctionSymbolSelection lastSelection = !ss_selections.isEmpty() ? ss_selections.get(ss_selections.size() - 1) : null;

        if (openPositionId != null){
            FunctionOpenPosition functionOpenPosition = new FunctionOpenPosition();
            functionOpenPosition.setOpenPositionId(openPositionId);
            List<FunctionOpenPosition> op_selection = functionOpenPositionService.selectFunctionOpenPositionList(functionOpenPosition);
            FunctionOpenPosition lastOpenPosition = !op_selection.isEmpty() ? op_selection.get(op_selection.size() - 1) : null;
            funMap.put("open_position", lastOpenPosition);
        }
        FunctionProfitLoss functionProfitLoss = new FunctionProfitLoss();
        functionProfitLoss.setProfitLossId(profitLossId);
        List<FunctionProfitLoss> pl_selections = functionProfitLossService.selectFunctionProfitLossList(functionProfitLoss);
        FunctionProfitLoss lastProfitLoss = !pl_selections.isEmpty() ? pl_selections.get(pl_selections.size() - 1) : null;


        FunctionFund functionFund = new FunctionFund();
        functionFund.setFundId(fundId);
        List<FunctionFund> fd_selections = functionFundService.selectFunctionFundList(functionFund);
        FunctionFund lastFund = !fd_selections.isEmpty() ? fd_selections.get(fd_selections.size() - 1) : null;
        funMap.put("symbol_selection", lastSelection);
        funMap.put("profit_loss", lastProfitLoss);
        funMap.put("fund", lastFund);
        String funJson = objectMapper.writeValueAsString(funMap);
        strategyBuild.setArgs(argsJson);
        strategyBuild.setFunDict(funJson);

        // 设置数据
        userStrategyAccount.setPosition(userStrategyPosition);
        userStrategyAccount.setOrders(userStrategyOrders);
        // 先执行添加策略

        strategyBuild.setId(strategy.getId());
        strategyBuild.setOwner(strategyOwner);
        strategyBuild.setAction(ADDSTRATEGY);
        strategyBuild.setLever(strategy.getLever());
        strategyBuild.setMaxPosition(strategy.getMaxPosition());
        strategyBuild.setAccount(accountJson);
        AjaxResult result = new AjaxResult(0, "addStrategy", strategyBuild);
        BaseResponse resp = pythonClient.sendDataToPython(result, BaseResponse.class);
        return resp.getMsg();
    }

    @Override
    public String runStrategy(StrategyBO strategyBO) {
        Long id = getaLong(strategyBO);
        if (id == null) return "非法操作，账户已封禁";
        BaseStrategy baseStrategy = new BaseStrategy();
        baseStrategy.setId(id);
        baseStrategy.setAction(RUNSTRATEGY);
        AjaxResult result = new AjaxResult(0, "runStrategy", baseStrategy);
        BaseResponse resp = pythonClient.sendDataToPython(result, BaseResponse.class);
        return resp.getMsg();
    }

    @Override
    public String removeStrategy(StrategyBO strategyBO) {
        Long id = getaLong(strategyBO);
        if (id == null) return "非法操作，账户已封禁";
        BaseStrategy baseStrategy = new BaseStrategy();
        baseStrategy.setId(id);
        baseStrategy.setAction(REMOVESTRATEGY);
        AjaxResult result = new AjaxResult(0, "removeStrategy", baseStrategy);
        BaseResponse resp = pythonClient.sendDataToPython(result, BaseResponse.class);
        return resp.getMsg();
    }

    @Override
    public Object operationInformation(StrategyBO strategyBO) {
        Long id = getaLong(strategyBO);
        if (id == null) return "非法操作，账户已封禁";
        BaseStrategy baseStrategy = new BaseStrategy();
        baseStrategy.setId(id);
        baseStrategy.setAction(OPERATIONINFORMATION);
        AjaxResult result = new AjaxResult(0, "operationInformation", baseStrategy);
        BaseResponse resp = pythonClient.sendDataToPython(result, BaseResponse.class);
        return resp.getData();
    }

    @Override
    public Object backTesting(BackTestingBO backTestingBO) {
        Long id = backTestingBO.getId(); // 策略id
        Long userId = SecurityUtils.getUserId(); // 用户id
        Strategy strategy = this.selectStrategyById(id);
        Long owner = strategy.getOwner();
        if (!userId.equals(owner)){
            SysUser sysUser = new SysUser();
            sysUser.setStatus("1");
            userService.updateUserStatus(sysUser);
            return "非法操作，账户已封禁";
        }
        AjaxResult result = new AjaxResult(0, BACKTESTING, backTestingBO);
        BaseResponse resp = pythonClient.sendDataToPython(result, BaseResponse.class);
        return resp.getData();
    }

    @Override
    public Object runningStrategies(StrategyBO strategyBO) {
        Long id = getaLong(strategyBO);
        if (id == null) return "非法操作，账户已封禁";
        BaseStrategy baseStrategy = new BaseStrategy();
        baseStrategy.setId(id);
        baseStrategy.setAction(RUNNINGSTRATEGIES);
        AjaxResult result = new AjaxResult(0, "running_strategy", baseStrategy);
        BaseResponse resp = pythonClient.sendDataToPython(result, BaseResponse.class);
        return resp.getData();
    }

    @Override
    public String initEngine() {
        BaseStrategy baseStrategy = new BaseStrategy();
        baseStrategy.setAction(INITENGINE);
        AjaxResult result = new AjaxResult(0, "init_engine", baseStrategy);
        BaseResponse resp = pythonClient.sendDataToPython(result, BaseResponse.class);
        return resp.getMsg();
    }

    @Override
    public String getOrders(StrategyBO strategyBO) {
        Long id = getaLong(strategyBO);
        BaseStrategy baseStrategy = new BaseStrategy();
        baseStrategy.setId(id);
        baseStrategy.setAction(GETORDERS);
        AjaxResult result = new AjaxResult(0, "get_orders", baseStrategy);
        BaseResponse resp = pythonClient.sendDataToPython(result, BaseResponse.class);
        return resp.getMsg();
    }

    @Override
    public String getPositions(StrategyBO strategyBO) {
        Long id = getaLong(strategyBO);
        BaseStrategy baseStrategy = new BaseStrategy();
        baseStrategy.setId(id);
        baseStrategy.setAction(GETPOSITIONS);
        AjaxResult result = new AjaxResult(0, "get_positions", baseStrategy);
        BaseResponse resp = pythonClient.sendDataToPython(result, BaseResponse.class);
        return resp.getMsg();
    }


    private Long getaLong(StrategyBO strategyBO) {
        Long userId = SecurityUtils.getUserId(); // 用户id
        Long id = strategyBO.getId(); // 策略id
        Strategy strategy = this.selectStrategyById(id);
        Long owner = strategy.getOwner();
        if (!userId.equals(owner)){
            SysUser sysUser = new SysUser();
            sysUser.setStatus("1");
            userService.updateUserStatus(sysUser);
            return null;
        }
        return id;
    }
}
