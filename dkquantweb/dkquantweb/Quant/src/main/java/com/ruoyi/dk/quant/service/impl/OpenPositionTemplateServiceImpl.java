package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.OpenPositionTemplateMapper;
import com.ruoyi.dk.quant.domain.OpenPositionTemplate;
import com.ruoyi.dk.quant.service.IOpenPositionTemplateService;

/**
 * 开仓策略模板Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
@Service
public class OpenPositionTemplateServiceImpl implements IOpenPositionTemplateService 
{
    @Autowired
    private OpenPositionTemplateMapper openPositionTemplateMapper;

    /**
     * 查询开仓策略模板
     * 
     * @param id 开仓策略模板主键
     * @return 开仓策略模板
     */
    @Override
    public OpenPositionTemplate selectOpenPositionTemplateById(Long id)
    {
        return openPositionTemplateMapper.selectOpenPositionTemplateById(id);
    }

    /**
     * 查询开仓策略模板列表
     * 
     * @param openPositionTemplate 开仓策略模板
     * @return 开仓策略模板
     */
    @Override
    public List<OpenPositionTemplate> selectOpenPositionTemplateList(OpenPositionTemplate openPositionTemplate)
    {
        return openPositionTemplateMapper.selectOpenPositionTemplateList(openPositionTemplate);
    }

    /**
     * 新增开仓策略模板
     * 
     * @param openPositionTemplate 开仓策略模板
     * @return 结果
     */
    @Override
    public int insertOpenPositionTemplate(OpenPositionTemplate openPositionTemplate)
    {
        return openPositionTemplateMapper.insertOpenPositionTemplate(openPositionTemplate);
    }

    /**
     * 修改开仓策略模板
     * 
     * @param openPositionTemplate 开仓策略模板
     * @return 结果
     */
    @Override
    public int updateOpenPositionTemplate(OpenPositionTemplate openPositionTemplate)
    {
        return openPositionTemplateMapper.updateOpenPositionTemplate(openPositionTemplate);
    }

    /**
     * 批量删除开仓策略模板
     * 
     * @param ids 需要删除的开仓策略模板主键
     * @return 结果
     */
    @Override
    public int deleteOpenPositionTemplateByIds(Long[] ids)
    {
        return openPositionTemplateMapper.deleteOpenPositionTemplateByIds(ids);
    }

    /**
     * 删除开仓策略模板信息
     * 
     * @param id 开仓策略模板主键
     * @return 结果
     */
    @Override
    public int deleteOpenPositionTemplateById(Long id)
    {
        return openPositionTemplateMapper.deleteOpenPositionTemplateById(id);
    }
}
