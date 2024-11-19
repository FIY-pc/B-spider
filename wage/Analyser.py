import re
class Parser:
    def __init__(self, path: str, weight: int = 0.5):
        self.path = path
        self.salary = []
        self.get_salary()
        self.average_salary(weight)
    def get_salary(self):
        with open(self.path, 'r', encoding='GBK') as f:
            data = f.read()
            pattern_salaryDesc = r"'salaryDesc': '(\d+-\d+K(?:·\d+薪)?)'"
            salary = re.findall(pattern_salaryDesc, data)
            self.salary = salary
    def average_salary(self,weight):
        salary = self.salary
        pattern_num = r"\d+-\d+K·(\d+)薪"
        pattern_low = r"(\d+)-\d+K"
        pattern_high = r"\d+-(\d)+K"

        total_average = 0
        for item in salary:
            low = re.findall(pattern_low, item)
            high = re.findall(pattern_high, item)
            num = re.findall(pattern_num, item)
            low = int(low[0])
            high = int(high[0])
            if num==[]:
                num = 12
            else:
                num = int(num[0])
            average = (low+high)*weight*num
            total_average += average
        average_all = total_average/len(salary)
        print("平均年薪", average_all, "K")



if __name__ == '__main__':
    parser = Parser('data/C++.txt')