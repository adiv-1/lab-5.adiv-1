import csv
from typing import Any, Dict, List, Tuple
from collections import Counter


def analyze_employee_data(filepath: str) -> Tuple[int, dict, str, List[Tuple[float, str]]]:
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        
        employee_count = 0
        male_count = 0
        female_count = 0
        entry_count = 0
        mid_count = 0
        senior_count = 0
        male_score = []
        female_score = []

        for item in reader:
            employee_count = employee_count + 1

            gender = item['Gender'].strip()
            solve = int(item['ProblemSolvingScore'].strip())

            if gender == 'Male':
                male_count += 1
                male_score.append(solve)
            elif gender == 'Female':
                female_count += 1
                female_score.append(solve)

            job_level = item['JobLevel'].strip()
            if job_level == 'Entry Level':
                entry_count += 1
            elif job_level == 'Mid Level':
                mid_count += 1
            elif job_level == 'Senior Level':
                senior_count += 1

        job_counts = {'Entry Level': entry_count, 'Mid Level': mid_count, 'Senior Level': senior_count}
        gender_count = {'Male': male_count, 'Female': female_count}

        most_common_job = sorted(job_counts.items(), key = lambda x: (-x[1], x[0]))[0][0]

        if male_score:
            highest_male = max(male_score)
        else:
            highest_male = None
        if female_score:
            highest_female = max(female_score)
        else:
            highest_female = None

        gender_score = []
        if highest_male is not None:
            gender_score.append((round(highest_male, 2), 'Male'))
        if highest_female is not None:
            gender_score.append((round(highest_female, 2), 'Female'))
            
        gender_score.sort(key = lambda x: (-x[0], x[1]))

        return employee_count, gender_count, most_common_job, gender_score


def analyze_sales_data(filepath: str) -> Tuple[Dict[str, int], Dict[str, float], float, List[str]]:
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)

        productcat_count = {}
        region_sales = {}
        region_count = {}
        maxsale_products = []
        maxsale_val = 0.0

        for item in reader:
            productcat = item['ProductCategory'].strip()
            sales = float(item['SaleAmount'].strip())
            region = item['SalesRegion'].strip()
            productid = item['ProductID'].strip()

            if productcat not in productcat_count:
                productcat_count[productcat] = 0
            productcat_count[productcat] += 1

            if region not in region_sales:
                region_sales[region] = 0.0
                region_count[region] = 0

            region_count[region] += 1
            region_sales[region] += sales

            if sales > maxsale_val:
                maxsale_val = sales
                maxsale_products = [productid]
            elif sales == maxsale_val:
                maxsale_products.append(productid)
        
        avg_region_sales = {region: round(region_sales[region] / region_count[region], 2) for region in region_sales}

        return productcat_count, avg_region_sales, maxsale_val, maxsale_products


def analyze_bank_data(filepath: str) -> Dict[str, Any]:
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)

        deposit_transact = []
        withdrawal_transact = []
        bank = {}

        for item in reader:
            trans_type = item['TransactionType'].strip()
            trans_desc = item['TransactionDescription'].strip().lower()

            if trans_type == 'Deposit':
                deposit_transact.append(trans_desc)
            elif trans_type == 'Withdrawal':
                withdrawal_transact.append(trans_desc)

        deposit_set = set(deposit_transact)
        withdrawal_set = set(withdrawal_transact)
        
        onlydep = list(deposit_set.difference(withdrawal_set))
        onlywith = list(withdrawal_set.difference(deposit_set))
        intersect = list(deposit_set.intersection(withdrawal_set))


        bank['only_deposit'] = onlydep
        bank['common'] = intersect
        bank['only_withdrawal'] = onlywith
        bank['exclusive_count'] = len(onlydep) + len(onlywith)

        return bank
