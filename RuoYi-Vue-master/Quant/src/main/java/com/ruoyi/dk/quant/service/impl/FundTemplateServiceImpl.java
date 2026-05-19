package com.ruoyi.dk.quant.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.dk.quant.mapper.FundTemplateMapper;
import com.ruoyi.dk.quant.domain.FundTemplate;
import com.ruoyi.dk.quant.service.IFundTemplateService;

/**
 * 资金策略模板Service业务层处理
 * 
 * @author ruoyi
 * @date 2025-03-18
 */
@Service
public class FundTemplateServiceImpl implements IFundTemplateService 
{
    @Autowired
    private FundTemplateMapper fundTemplateMapper;

    /**
     * 查询资金策略模板
     * 
     * @param id 资金策略模板主键
     * @return 资金策略模板
     */
    @Override
    public FundTemplate selectFundTemplateById(Long id)
    {
        return fundTemplateMapper.selectFundTemplateById(id);
    }

    /**
     * 查询资金策略模板列表
     * 
     * @param fundTemplate 资金策略模板
     * @return 资金策略模板
     */
    @Override
    public List<FundTemplate> selectFundTemplateList(FundTemplate fundTemplate)
    {
        return fundTemplateMapper.selectFundTemplateList(fundTemplate);
    }

    /**
     * 新增资金策略模板
     * 
     * @param fundTemplate 资金策略模板
     * @return 结果
     */
    @Override
    public int insertFundTemplate(FundTemplate fundTemplate)
    {
        return fundTemplateMapper.insertFundTemplate(fundTemplate);
    }

    /**
     * 修改资金策略模板
     * 
     * @param fundTemplate 资金策略模板
     * @return 结果
     */
    @Override
    public int updateFundTemplate(FundTemplate fundTemplate)
    {
        return fundTemplateMapper.updateFundTemplate(fundTemplate);
    }

    /**
     * 批量删除资金策略模板
     * 
     * @param ids 需要删除的资金策略模板主键
     * @return 结果
     */
    @Override
    public int deleteFundTemplateByIds(Long[] ids)
    {
        return fundTemplateMapper.deleteFundTemplateByIds(ids);
    }

    /**
     * 删除资金策略模板信息
     * 
     * @param id 资金策略模板主键
     * @return 结果
     */
    @Override
    public int deleteFundTemplateById(Long id)
    {
        return fundTemplateMapper.deleteFundTemplateById(id);
    }
}
