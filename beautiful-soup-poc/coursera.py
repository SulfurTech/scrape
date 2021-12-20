from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium import webdriver


def find_courses(source):
    pgcn = BeautifulSoup(source, 'html.parser')
    if pgcn is None:
        print("Page not found")
    else:
        courses = pgcn.find_all("li", {'class': 'ais-InfiniteHits-item'})
        for course in courses:
            try:
                course_title = course.h2.get_text()
                course_rating = course.find('span', {'class': 'ratings-text'}). \
                    get_text()
                print(f"Course Title: \t {course_title}")
                print(f"Course Rating: \t {course_rating}")
                print('\n' + '|' + ('<' * 3) + ('-' * 7) + ' New Course ' + ('-' * 7) + ('>' * 3) + '|' + '\n')
            except:
                print("Something went wrong when printing the courses")

url = "https://www.coursera.org/courses?query=&indices%5Bprod_all_products_term_optimization_test%5D%5Bpage%5D=1&indices%5Bprod_all_products_term_optimization_test%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products_term_optimization_test%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true"
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(80)
for i in range(3):
    element = driver.find_element_by_id('pagination_right_arrow_button')
    ActionChains(driver).move_to_element(element).perform()
    find_courses(driver.page_source)
    ActionChains(driver).click().perform()
    driver.implicitly_wait(80)
driver.quit()