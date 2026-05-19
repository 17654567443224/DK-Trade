package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.StrategyDes;

/**
 * 策略描述Mapper接口
 * 
 * @author ruoyi
 * @date 2025-03-31
 */
public interface StrategyDesMapper 
{
    /**
     * 查询策略描述
     * 
     * @param id 策略描述主键
     * @return 策略描述
     */
    public StrategyDes selectStrategyDesById(Long id);

    /**
     * 查询策略描述列表
     * 
     * @param strategyDes 策略描述
     * @return 策略描述集合
     */
    public List<StrategyDes> selectStrategyDesList(StrategyDes strategyDes);

    /**
     * 新增策略描述
     * 
     * @param strategyDes 策略描述
     * @return 结果
     */
    public int insertStrategyDes(StrategyDes strategyDes);

    /**
     * 修改策略描述
     * 
     * @param strategyDes 策略描述
     * @return 结果
     */
    public int updateStrategyDes(StrategyDes strategyDes);

    /**
     * 删除策略描述
     * 
     * @param id 策略描述主键
     * @return 结果
     */
    public int deleteStrategyDesById(Long id);

    /**
     * 批量删除策略描述
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteStrategyDesByIds(Long[] ids);
}
