package com.ruoyi.dk.quant.mapper;

import java.util.List;
import com.ruoyi.dk.quant.domain.OpenPositionTemplate;

/**
 * 开仓策略模板Mapper接口
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
public interface OpenPositionTemplateMapper 
{
    /**
     * 查询开仓策略模板
     * 
     * @param id 开仓策略模板主键
     * @return 开仓策略模板
     */
    public OpenPositionTemplate selectOpenPositionTemplateById(Long id);

    /**
     * 查询开仓策略模板列表
     * 
     * @param openPositionTemplate 开仓策略模板
     * @return 开仓策略模板集合
     */
    public List<OpenPositionTemplate> selectOpenPositionTemplateList(OpenPositionTemplate openPositionTemplate);

    /**
     * 新增开仓策略模板
     * 
     * @param openPositionTemplate 开仓策略模板
     * @return 结果
     */
    public int insertOpenPositionTemplate(OpenPositionTemplate openPositionTemplate);

    /**
     * 修改开仓策略模板
     * 
     * @param openPositionTemplate 开仓策略模板
     * @return 结果
     */
    public int updateOpenPositionTemplate(OpenPositionTemplate openPositionTemplate);

    /**
     * 删除开仓策略模板
     * 
     * @param id 开仓策略模板主键
     * @return 结果
     */
    public int deleteOpenPositionTemplateById(Long id);

    /**
     * 批量删除开仓策略模板
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteOpenPositionTemplateByIds(Long[] ids);
}
