package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.Strategy;

/**
 * 策略Mapper接口
 * 
 * @author ruoyi
 * @date 2025-02-16
 */
public interface StrategyMapper 
{
    /**
     * 查询策略
     * 
     * @param id 策略主键
     * @return 策略
     */
    public Strategy selectStrategyById(Long id);

    /**
     * 查询策略列表
     * 
     * @param strategy 策略
     * @return 策略集合
     */
    public List<Strategy> selectStrategyList(Strategy strategy);

    /**
     * 新增策略
     * 
     * @param strategy 策略
     * @return 结果
     */
    public int insertStrategy(Strategy strategy);

    /**
     * 修改策略
     * 
     * @param strategy 策略
     * @return 结果
     */
    public int updateStrategy(Strategy strategy);

    /**
     * 删除策略
     * 
     * @param id 策略主键
     * @return 结果
     */
    public int deleteStrategyById(Long id);

    /**
     * 批量删除策略
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteStrategyByIds(Long[] ids);
}
